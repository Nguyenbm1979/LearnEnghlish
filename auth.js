// Đăng nhập bằng Google + đồng bộ tiến độ học lên Firebase (Firestore).
// Tự động TẮT hoàn toàn nếu firebase-config.js chưa được điền giá trị thật —
// khi đó app chạy y như cũ (không tải Firebase SDK, không có tường đăng nhập).
const cfg = window.FIREBASE_CONFIG || {};
const isConfigured = !!(cfg.apiKey && cfg.apiKey !== "YOUR_API_KEY");

if (!isConfigured) {
  console.info("[auth] Firebase chưa được cấu hình (firebase-config.js) — bỏ qua đăng nhập, app chạy như bình thường.");
} else {
  const [{ initializeApp }, { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged }, { getFirestore, doc, getDoc, setDoc }] =
    await Promise.all([
      import("https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js"),
      import("https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js"),
      import("https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore.js"),
    ]);

  const app = initializeApp(cfg);
  const auth = getAuth(app);
  const db = getFirestore(app);
  const provider = new GoogleAuthProvider();

  const HISTORY_KEY = "eng_history_v1";
  let currentUser = null;

  function mergeHistory(a, b) {
    const out = { ...a };
    for (const date in b) out[date] = { ...(out[date] || {}), ...b[date] };
    return out;
  }

  function refreshAppUI() {
    if (window.updateStreak) window.updateStreak();
    if (window.renderProgress) window.renderProgress();
  }

  async function syncFromCloud(user) {
    const ref = doc(db, "users", user.uid);
    const snap = await getDoc(ref);
    const local = JSON.parse(localStorage.getItem(HISTORY_KEY) || "{}");
    const cloud = snap.exists() ? (snap.data().history || {}) : {};
    const merged = mergeHistory(local, cloud);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(merged));
    await setDoc(ref, {
      history: merged,
      email: user.email || "",
      name: user.displayName || "",
      updatedAt: Date.now()
    }, { merge: true });
    refreshAppUI();
  }

  function showGate() {
    const gate = document.getElementById("authGate");
    if (gate) gate.style.display = "flex";
    const box = document.getElementById("accountBox");
    if (box) box.style.display = "none";
  }

  function hideGate() {
    const gate = document.getElementById("authGate");
    if (gate) gate.style.display = "none";
  }

  function renderAccountBox(user) {
    const box = document.getElementById("accountBox");
    if (!box) return;
    box.style.display = "flex";
    box.innerHTML = `
      <span class="muted" style="font-size:.8rem">👤 ${user.displayName || user.email || "Học viên"}</span>
      <button class="ghost" style="padding:5px 10px;font-size:.78rem" id="signOutBtn">Đăng xuất</button>`;
    document.getElementById("signOutBtn").onclick = () => signOut(auth);
  }

  onAuthStateChanged(auth, async (user) => {
    currentUser = user;
    if (user) {
      hideGate();
      renderAccountBox(user);
      await syncFromCloud(user);
    } else {
      showGate();
    }
  });

  window.__pushProgressToCloud = async function () {
    if (!currentUser) return;
    try {
      const local = JSON.parse(localStorage.getItem(HISTORY_KEY) || "{}");
      await setDoc(doc(db, "users", currentUser.uid), { history: local, updatedAt: Date.now() }, { merge: true });
    } catch (e) {
      console.error("[auth] Không đồng bộ được tiến độ lên Firebase:", e);
    }
  };

  window.__signInGoogle = async function () {
    try {
      await signInWithPopup(auth, provider);
    } catch (e) {
      alert("Đăng nhập thất bại: " + e.message);
    }
  };
}
