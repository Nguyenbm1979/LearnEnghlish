// Truyện cổ tích kinh điển cho thiếu nhi học tiếng Anh — câu ngắn, dễ hiểu.
// Ảnh minh họa thật lấy từ Wikimedia Commons (public domain).
// Đọc bằng giọng đọc trình duyệt có sẵn (Web Speech API), không cần mạng.
const STORY_BANK = [
  {
    title_en: "The Three Little Pigs",
    title_vi: "Ba Chú Lợn Con",
    image: "https://upload.wikimedia.org/wikipedia/commons/e/e3/Queerie_Queers_-_Three_Little_Pigs_002.png",
    pages: [
      { en: "Once upon a time, there were three little pigs.", vi: "Ngày xửa ngày xưa, có ba chú lợn con." },
      { en: "They left home to build their own houses.", vi: "Chúng rời nhà để tự xây nhà cho mình." },
      { en: "The first pig built a house of straw. It was very fast.", vi: "Chú lợn thứ nhất xây nhà bằng rơm. Rất nhanh." },
      { en: "The second pig built a house of sticks.", vi: "Chú lợn thứ hai xây nhà bằng gỗ que." },
      { en: "The third pig worked hard and built a house of bricks.", vi: "Chú lợn thứ ba chăm chỉ xây nhà bằng gạch." },
      { en: "A big bad wolf came. He blew down the straw house!", vi: "Một con sói lớn xấu xa xuất hiện. Nó thổi bay nhà rơm!" },
      { en: "He blew down the stick house too. The two pigs ran to their brother.", vi: "Nó cũng thổi bay nhà gỗ que. Hai chú lợn chạy đến nhà anh mình." },
      { en: "The wolf could not blow down the brick house. The three pigs were safe.", vi: "Sói không thể thổi bay nhà gạch. Ba chú lợn được an toàn." }
    ]
  },
  {
    title_en: "Goldilocks and the Three Bears",
    title_vi: "Goldilocks Và Ba Chú Gấu",
    image: "https://upload.wikimedia.org/wikipedia/commons/c/c5/Jessie_Willcox_Smith_-_%27Goldilocks_and_the_Three_Bears%27%2C_Swift%27s_Premium_Soap_Products_calendar_illustration.jpg",
    pages: [
      { en: "A little girl named Goldilocks walked into the forest.", vi: "Một cô bé tên Goldilocks đi vào rừng." },
      { en: "She found a little house. No one answered, so she went in.", vi: "Cô tìm thấy một ngôi nhà nhỏ. Không ai trả lời, nên cô bước vào." },
      { en: "On the table were three bowls of soup: big, medium, and small.", vi: "Trên bàn có ba bát súp: to, vừa và nhỏ." },
      { en: "The small bowl was just right, so she ate it all.", vi: "Bát nhỏ vừa vặn, nên cô ăn hết sạch." },
      { en: "She tried three chairs. The small chair broke!", vi: "Cô thử ba cái ghế. Chiếc ghế nhỏ bị gãy!" },
      { en: "She was sleepy, so she tried three beds. The small bed was perfect.", vi: "Cô buồn ngủ, nên thử ba chiếc giường. Giường nhỏ rất vừa vặn." },
      { en: "Then the three bears came home and found her sleeping!", vi: "Rồi ba chú gấu về nhà và thấy cô đang ngủ!" },
      { en: "Goldilocks woke up, jumped out of the window, and ran home.", vi: "Goldilocks tỉnh dậy, nhảy qua cửa sổ và chạy về nhà." }
    ]
  },
  {
    title_en: "Little Red Riding Hood",
    title_vi: "Cô Bé Quàng Khăn Đỏ",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Little_Red_Riding_Hood_-_J._W._Smith.jpg/960px-Little_Red_Riding_Hood_-_J._W._Smith.jpg",
    pages: [
      { en: "A little girl always wore a red hood, so people called her Little Red Riding Hood.", vi: "Một cô bé luôn đội khăn đỏ, nên mọi người gọi cô là Cô Bé Quàng Khăn Đỏ." },
      { en: "One day, she walked through the forest to visit her sick grandmother.", vi: "Một ngày nọ, cô đi qua rừng để thăm bà bị ốm." },
      { en: "A sneaky wolf saw her and asked where she was going.", vi: "Một con sói ranh mãnh thấy cô và hỏi cô đi đâu." },
      { en: "The wolf ran ahead to grandmother's house and hid inside.", vi: "Con sói chạy trước đến nhà bà và trốn bên trong." },
      { en: "Little Red Riding Hood arrived. 'Grandma, what big eyes you have!'", vi: "Cô Bé Quàng Khăn Đỏ đến nơi. 'Bà ơi, mắt bà to quá!'" },
      { en: "'All the better to see you with!' said the wolf.", vi: "'Để bà nhìn cháu rõ hơn!' con sói nói." },
      { en: "A woodcutter heard the noise and rushed in to help.", vi: "Một bác tiều phu nghe thấy tiếng động và chạy vào giúp." },
      { en: "The wolf ran away, and everyone was safe again.", vi: "Con sói bỏ chạy, và mọi người lại được an toàn." }
    ]
  },
  {
    title_en: "The Tortoise and the Hare",
    title_vi: "Rùa Và Thỏ",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Tortoise_and_hare_rackham.jpg/960px-Tortoise_and_hare_rackham.jpg",
    pages: [
      { en: "A hare loved to boast that he was the fastest animal in the forest.", vi: "Một chú thỏ thích khoe rằng mình là con vật nhanh nhất trong rừng." },
      { en: "A slow tortoise said, 'I challenge you to a race.'", vi: "Một chú rùa chậm chạp nói, 'Tôi thách anh chạy đua.'" },
      { en: "All the animals gathered to watch the race begin.", vi: "Tất cả các con vật tụ tập để xem cuộc đua bắt đầu." },
      { en: "The hare ran far ahead and felt very sure he would win.", vi: "Thỏ chạy vượt lên rất xa và cảm thấy chắc chắn sẽ thắng." },
      { en: "He decided to rest under a tree. 'I have plenty of time,' he thought.", vi: "Nó quyết định nghỉ dưới gốc cây. 'Mình còn nhiều thời gian mà,' nó nghĩ." },
      { en: "The hare fell fast asleep in the warm sun.", vi: "Thỏ ngủ say dưới ánh nắng ấm áp." },
      { en: "The tortoise kept walking, slow and steady, past the sleeping hare.", vi: "Rùa vẫn tiếp tục đi, chậm mà chắc, qua mặt chú thỏ đang ngủ." },
      { en: "The hare woke up too late. The tortoise had already won the race!", vi: "Thỏ tỉnh dậy thì đã quá muộn. Rùa đã thắng cuộc đua!" }
    ]
  },
  {
    title_en: "The Ugly Duckling",
    title_vi: "Chú Vịt Con Xấu Xí",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/The_Ugly_Duckling.jpg/960px-The_Ugly_Duckling.jpg",
    pages: [
      { en: "A mother duck's eggs hatched, but one baby bird looked very different.", vi: "Trứng của mẹ vịt nở ra, nhưng có một con chim con trông rất khác." },
      { en: "The other ducklings laughed and called him ugly.", vi: "Những chú vịt con khác cười nhạo và gọi cậu là xấu xí." },
      { en: "Feeling sad and lonely, the little bird ran away from the farm.", vi: "Cảm thấy buồn và cô đơn, chú chim nhỏ chạy trốn khỏi trang trại." },
      { en: "He spent a long, cold winter alone, hiding from other animals.", vi: "Cậu trải qua một mùa đông dài, lạnh lẽo một mình, trốn tránh các con vật khác." },
      { en: "In spring, he saw beautiful white swans swimming on the lake.", vi: "Đến mùa xuân, cậu thấy những chú thiên nga trắng đẹp đẽ bơi trên hồ." },
      { en: "He swam toward them, ready to be laughed at again.", vi: "Cậu bơi về phía chúng, sẵn sàng bị cười nhạo lần nữa." },
      { en: "But when he looked at the water, he saw his own reflection.", vi: "Nhưng khi nhìn xuống mặt nước, cậu thấy hình ảnh của chính mình." },
      { en: "He was not a duckling at all — he had grown into a beautiful swan!", vi: "Cậu không phải là vịt con — cậu đã lớn thành một chú thiên nga xinh đẹp!" }
    ]
  },
  {
    title_en: "Cinderella",
    title_vi: "Cô Bé Lọ Lem",
    image: "https://upload.wikimedia.org/wikipedia/commons/7/79/MU_KPB_022_Cinderella_-_Arthur_Rackham_11.jpg",
    pages: [
      { en: "Cinderella lived with her stepmother and two unkind stepsisters.", vi: "Cô bé Lọ Lem sống cùng mẹ kế và hai người chị kế không tốt bụng." },
      { en: "She had to do all the housework while they rested.", vi: "Cô phải làm hết việc nhà trong khi họ nghỉ ngơi." },
      { en: "One day, the King invited everyone to a grand ball at the palace.", vi: "Một ngày nọ, Nhà Vua mời mọi người đến một buổi dạ hội lớn ở cung điện." },
      { en: "Cinderella's stepsisters went, but she was left behind, crying.", vi: "Hai chị kế của Lọ Lem đi dự, nhưng cô bị bỏ lại, khóc một mình." },
      { en: "A kind fairy godmother appeared and made her a beautiful dress.", vi: "Một bà tiên tốt bụng xuất hiện và may cho cô một chiếc váy xinh đẹp." },
      { en: "'You must return before midnight,' the fairy warned her.", vi: "'Con phải về trước nửa đêm,' bà tiên dặn dò." },
      { en: "At the ball, the Prince danced with her all night, but at midnight she ran away, losing one glass slipper.", vi: "Tại dạ hội, Hoàng tử khiêu vũ với cô suốt đêm, nhưng đến nửa đêm cô chạy đi, đánh rơi một chiếc giày thủy tinh." },
      { en: "The Prince searched the kingdom and found her. They lived happily ever after.", vi: "Hoàng tử tìm khắp vương quốc và tìm thấy cô. Họ sống hạnh phúc mãi mãi." }
    ]
  },
  {
    title_en: "Hansel and Gretel",
    title_vi: "Hansel Và Gretel",
    image: "https://upload.wikimedia.org/wikipedia/commons/d/d1/Hansel-and-gretel-rackham.jpg",
    pages: [
      { en: "Hansel and Gretel were a brother and sister who lived near a forest.", vi: "Hansel và Gretel là hai anh em sống gần một khu rừng." },
      { en: "One day, they got lost deep in the woods.", vi: "Một ngày nọ, họ bị lạc sâu trong rừng." },
      { en: "They found a little house made of candy and cake!", vi: "Họ tìm thấy một ngôi nhà nhỏ làm bằng kẹo và bánh!" },
      { en: "They began to eat it, but an old witch lived inside.", vi: "Họ bắt đầu ăn ngôi nhà, nhưng một mụ phù thủy già sống bên trong." },
      { en: "The witch was not kind at all — she wanted to trap them.", vi: "Mụ phù thủy chẳng tốt bụng chút nào — bà ta muốn bẫy họ." },
      { en: "Clever Gretel tricked the witch and pushed her into the oven.", vi: "Gretel thông minh đánh lừa mụ phù thủy và đẩy bà ta vào lò." },
      { en: "The children found treasure in the witch's house.", vi: "Hai anh em tìm thấy kho báu trong nhà mụ phù thủy." },
      { en: "They carried it home and lived happily with their father.", vi: "Họ mang kho báu về nhà và sống hạnh phúc cùng cha." }
    ]
  },
  {
    title_en: "Jack and the Beanstalk",
    title_vi: "Jack Và Cây Đậu Thần",
    image: "https://upload.wikimedia.org/wikipedia/commons/b/be/Jack_and_the_Beanstalk_Cruikshank_1854.jpg",
    pages: [
      { en: "Jack and his mother were poor, so they had to sell their cow.", vi: "Jack và mẹ nghèo khó, nên phải bán con bò của mình." },
      { en: "On the way to town, a man traded Jack magic beans for the cow.", vi: "Trên đường ra chợ, một người đàn ông đổi cho Jack những hạt đậu thần lấy con bò." },
      { en: "Jack's mother was angry and threw the beans out the window.", vi: "Mẹ Jack rất giận và ném những hạt đậu ra cửa sổ." },
      { en: "By morning, a giant beanstalk had grown up into the clouds!", vi: "Đến sáng, một cây đậu khổng lồ đã mọc cao lên tận mây!" },
      { en: "Jack climbed all the way up and found a castle in the sky.", vi: "Jack trèo lên tận nơi và tìm thấy một lâu đài trên trời." },
      { en: "A giant lived there with bags of gold and a hen that laid golden eggs.", vi: "Một người khổng lồ sống ở đó với những bao vàng và một con gà mái đẻ trứng vàng." },
      { en: "Jack took the golden hen and climbed back down quickly.", vi: "Jack lấy con gà vàng và nhanh chóng trèo xuống." },
      { en: "He chopped down the beanstalk, and he and his mother were never poor again.", vi: "Cậu chặt cây đậu, và từ đó cậu và mẹ không bao giờ nghèo khó nữa." }
    ]
  }
];
