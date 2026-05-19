import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

characters = [
    {
        "name": "神尾观铃",
        "img": "https://i.postimg.cc/tCTy7j1f/4a2a1211b263412c7d0f25d7a2fbdc4b.jpg",
    },
    {
        "name": "满穗",
        "img": "https://i.postimg.cc/25pfHLHR/535e82c17d20c79cf620a97f6d4af134-720.jpg",
    },
    {
        "name": "小满",
        "img": "https://i.postimg.cc/XqvMZfvF/73ef7f372afcdcc1583e967bbb500b23-720.jpg",
    },
    {
        "name": "夙川惠璃",
        "img": "https://i.postimg.cc/bwt72Nq6/07e7e6f1954d05f5d29a9626620f4c5b.jpg",
    },
    {
        "name": "朝武芳乃",
        "img": "https://i.postimg.cc/5tmkwXTm/df9199eec146797d099075ae72789a57.jpg",
    },
    {
        "name": "天宮寺・華恋",
        "img": "https://i.postimg.cc/XJHHzTVG/a2444428688445daaf0d26d4d8c35b1a-720.png",
    },
    {
        "name": "御坂美琴（mikoto misaka）",
        "img": "https://i.postimg.cc/0NZczLKW/wp7643656-mikoto-misaka-wallpapers.jpg",
    },
    {
        "name": "卡拉·西尔维亚·奎尼伯恩",
        "img": "https://i.postimg.cc/FHgCdm7D/1348fe231efa023c0a1e0268ae1c351e-720.png",
    },
    {
        "name": "紬文德斯",
        "img": "https://i.postimg.cc/k4cD7qxn/096ddb8a7db71914003bf28107fd8a4a-720.jpg",
    },
    {
        "name": "墨染希",
        "img": "https://i.postimg.cc/W40hfMzq/b831eff6806178160bdd3b6203e07fe7-720.jpg",
    },
    {
        "name": "绫地宁宁",
        "img": "https://i.postimg.cc/c45gKxPC/16c9611ff47a877e851fbb43091b1991-720.jpg",
    },
    {
        "name": "朵鲁蒂尼妲·费瑞",
        "img": "https://i.postimg.cc/s2TtzLvk/69fc5139fac5584b2fa4eeffd21a379f-720.jpg",
    },
    {
        "name": "黎瑟西雅·帕萨里利",
        "img": "https://i.postimg.cc/XY3hCWFM/26ebf1da5869f3b3fe259235fa255c04-720.jpg",
    },
    {
        "name": "雅俐耶妲·费瑞",
        "img": "https://i.postimg.cc/VNkVKFDD/e6eb979ce6eb12024b4ab25464678de9-720.jpg",
    },
    {
        "name": "芙铃",
        "img": "https://i.postimg.cc/g0tBQ67d/40753ca75a354459f151fe9cd8604221.jpg",
    },
    {
        "name": "上坂茅羽耶",
        "img": "https://i.postimg.cc/bJKVNf8B/febda443898d42a091c07c488a7b886c-720.png",
    },
    {
        "name": "二条院羽月",
        "img": "https://i.postimg.cc/d0h97NWP/b8b5ec28370aeae5cfa26d1708d905db-720.jpg",
    },
    {
        "name": "椎叶䌷",
        "img": "https://i.postimg.cc/nhP4tYnd/ad5df3b4d86d72f08e092c35387147ad-720.jpg",
    },
    {
        "name": "鹭泽有里栖",
        "img": "https://i.postimg.cc/mZKJgJzy/291cb0bee06c6e8156f636f025137220-720.jpg",
    },
    {
        "name": "平坂景子",
        "img": "https://i.postimg.cc/1XLQybVN/e7f711249779acf44fb90336472030fb.jpg",
    },
    {
        "name": "水澄华实",
        "img": "https://i.postimg.cc/T11KcY5M/a91416c2d1b927d58200efc0b893321f-720.jpg",
    },
    {
        "name": "天河沙夜",
        "img": "https://i.postimg.cc/VNsj8b4P/b452c9bb5685fc73e5f18600962be233.jpg",
    },
    {
        "name": "小木曾雪菜",
        "img": "https://i.postimg.cc/rsrCfZkw/435-CC2-BC453-E4-CC3368-A9-A97-E6-FBBC02.jpg",
    },
    {
        "name": "绯宫绫梨",
        "img": "https://i.postimg.cc/bJqbsxfD/025eeadda348087973a4645fc34bee99-720.jpg",
    },
    {
        "name": "中津静流",
        "img": "https://i.postimg.cc/50vwKjMn/e8065af4e90b4f17b21ebb09dc83c00b-720.jpg",
    },
    {
        "name": "安和昴",
        "img": "https://i.postimg.cc/4xqDghpG/cc8aff5a79f4e0823d6178a881150225.webp",
    },
    {
        "name": "金色暗影",
        "img": "https://i.postimg.cc/sxj8cPCY/35c75a515a0dd0d9d7d059bc368d0cb3.jpg",
    },
    {
        "name": "乾纱凪",
        "img": "https://i.postimg.cc/XNZ1vDx0/66b11e54cb26275b91c713c73d8c056b-720.jpg",
    },
    {
        "name": "雪村李",
        "img": "https://i.postimg.cc/L6wPvxM2/c0b5e69d8983b200f34043d7757b0faa-720.jpg",
    },
    {
        "name": "夜刀神十香",
        "img": "https://i.postimg.cc/5N1TnvKZ/048a7787e80eef37d24b6005205e48bc.jpg",
    },
    {
        "name": "仮屋和奏",
        "img": "https://i.postimg.cc/FRXMJtyM/655b18e9a9047664ccfdee03d79a92f1.jpg",
    },
    {
        "name": "仮屋和奏",
        "img": "https://i.postimg.cc/7PVFbWfR/1cba8951076ed7f558b532f36bd32e27.jpg",
    },
    {
        "name": "菲娅",
        "img": "https://i.postimg.cc/1RJgXmdG/39c83e97ca552c13d8b87168a47fceda-720.jpg",
    },
    {
        "name": "有濑川阿尔尔",
        "img": "https://i.postimg.cc/qBcyQ3B8/46f7bc8b9e7b8b6f77d9a9b738afadd1-720.jpg",
    },
    {
        "name": "飞鸟凑",
        "img": "https://i.postimg.cc/xTtHVVz8/0a2c31ddd17ed72f51d20b1613631258-720.jpg",
    },
    {
        "name": "绫崎优",
        "img": "https://i.postimg.cc/L8W1hkvM/e0cb3af697a9b66fb7c6a5ac412c82ef-720.jpg",
    },
    {
        "name": "桐谷梨梨爱",
        "img": "https://i.postimg.cc/R0nnt3bJ/2c01221b70e32adf535793c479aebd0d-720.jpg",
    },
    {
        "name": "春日野穹",
        "img": "https://i.postimg.cc/Hk4dfbwW/28dd223e9f83020a3cc7197b21d6409b-720.jpg",
    },
    {
        "name": "远野恋",
        "img": "https://i.postimg.cc/MpkGkWg5/9fbc32b1771500a00bedb7eec31d8229-720.jpg",
    },
    {
        "name": "夏玛拉",
        "img": "https://i.postimg.cc/3NVxx7NK/1d83a305b47956b3059254d2598c44a4.jpg",
    },
    {
        "name": "笼女",
        "img": "https://i.postimg.cc/NGJynvgC/be4dda33d125ab31f50da96e8070c8c1-720.jpg",
    },
    {
        "name": "明日美",
        "img": "https://i.postimg.cc/d19C37cJ/90cb23346b9dd80a5d286c57a9c425aa-720.jpg",
    },
    {
        "name": "菲莉娅",
        "img": "https://i.postimg.cc/1znM8rvs/f58bbdc0171ecc233d4dfdab80596e8f-720.jpg",
    },
    {
        "name": "神挂由岐奈",
        "img": "https://i.postimg.cc/X7srTS4D/475221513a54d1dec0de36449d577430-720.jpg",
    },
    {
        "name": "月見坂桐葉",
        "img": "https://i.postimg.cc/t47sbSgR/9e8f56a1dffb8c02c3bfe834102d1222.jpg",
    },
    {
        "name": "泽井须美",
        "img": "https://i.postimg.cc/NF7HyKhg/092bfdf2d8f487dc90b640618f78be68.jpg",
    },
    {
        "name": "泽井爱丽丝",
        "img": "https://i.postimg.cc/CLS83sDd/dcb58de081515425e143abfe7475e847.jpg",
    },
    {
        "name": "猫天宫花子[泳装]",
        "img": "https://i.postimg.cc/d0kZ2HMN/a860c3a3a7b93db6364db21955db669a-720.jpg",
    },
    {
        "name": "猫天宫花子",
        "img": "https://i.postimg.cc/ZnZ9hJWX/1a5771b825239617043eaac332855298.jpg",
    },
    {
        "name": "萨缇娅",
        "img": "https://i.postimg.cc/0QkZ21KK/51dede98129e0007424eb67e77c2d1af-720.jpg",
    },
    {
        "name": "艾露露",
        "img": "https://i.postimg.cc/8zGZnvkb/16bfd4ab81c59cec075485a7fe8babb0.jpg",
    },
    {
        "name": "美浜羊",
        "img": "https://i.postimg.cc/50XgFqpf/f7965c0610fa4de4b22bb4b73f4ef27a-720.jpg",
    },
    {
        "name": "藤见环",
        "img": "https://i.postimg.cc/hjNr8z3T/1502d7c8c685992c57e11fafb11a5c16.jpg",
    },
    {
        "name": "仁礼栖香",
        "img": "https://i.postimg.cc/gc64zsnD/eff40a1fa9980e4f5f9145762897b9f8-720.jpg",
    },
    {
        "name": "泽井夏叶",
        "img": "https://i.postimg.cc/x8rC3nGc/1e05b384e4bf760197e6916e1a4b19c1-720.jpg",
    },
    {
        "name": "彩濑逢樱[春]",
        "img": "https://i.postimg.cc/Fzg9bcsB/5573f9a3b32ccdb17d3ab0458247d524-720.jpg",
    },
    {
        "name": "彩濑逢樱[夏]",
        "img": "https://i.postimg.cc/T2rYX8qJ/bb6adac3f122fe0ce93a4c1aa7c815e7-720.jpg",
    },
    {
        "name": "彩濑逢樱[秋]",
        "img": "https://i.postimg.cc/wvDHHJJj/46ea687bfa71e5f3537ec0a856f2da8e-720.jpg",
    },
    {
        "name": "凪间梦未",
        "img": "https://i.postimg.cc/Sx5pMVfK/e8ec4ad27020b074075ad38d5ff99e69-720.jpg",
    },
    {
        "name": "雪妃艾琳娜",
        "img": "https://i.postimg.cc/Dfgkg7PH/10da3d9dd3ca9ab38081fe185fa89a79.jpg",
    },
    {
        "name": "吹雪",
        "img": "https://i.postimg.cc/02Q30DQK/4146ce6750e87c1cc996d39965d72358.jpg",
    },
    {
        "name": "女未茜",
        "img": "https://i.postimg.cc/C5TmbnzX/00f9a10cdad32e4a8198567e0e681632-720.jpg",
    },
    {
        "name": "女未空",
        "img": "https://i.postimg.cc/L8NCGsbg/2061fce4d39e75a9f25de8005da56c89-720.jpg",
    },
    {
        "name": "右田铃",
        "img": "https://i.postimg.cc/XNzvN7Sd/5273ea5998dbedbd583c36bdc091f01f-720.jpg",
    },
    {
        "name": "女未琥珀",
        "img": "https://i.postimg.cc/W4BVZt8J/c1bf924e2f12bd4f432d51b888981664.jpg",
    },
    {"name": "四季夏目", "img": "https://ps.ssl.qhimg.com/t0267cfef97ef44c1e5.jpg"},
    {"name": "雪村千绘莉", "img": "https://ps.ssl.qhimg.com/t025e9751dd2978c0be.jpg"},
    {
        "name": "冬月十夜",
        "img": "https://1.z.wiki/autoupload/20250525/4frl/5120X2880/%E5%86%AC%E6%9C%88_%E5%8D%81%E5%A4%9C.png",
    },
    {"name": "久岛鸥", "img": "https://ps.ssl.qhimg.com/t0287d5c9ee73dbf154.jpg"},
    {"name": "天宫美久栗", "img": "https://ps.ssl.qhimg.com/t020807388053360548.jpg"},
    {"name": "萤 铃音", "img": "https://ps.ssl.qhimg.com/t02cb6166856fc60c6b.jpg"},
    {"name": "白河灯莉", "img": "https://ps.ssl.qhimg.com/t027366273d0b491232.jpg"},
    {"name": "城崎绚华", "img": "https://ps.ssl.qhimg.com/t02df922c8aa8a92d27.jpg"},
    {"name": "镰仓 诗樱", "img": "https://ps.ssl.qhimg.com/t02bb0b46e1c05f4b09.jpg"},
    {"name": "凜堂耶", "img": "https://ps.ssl.qhimg.com/t02e6f2a56c38bfb739.jpg"},
    {"name": "神山识", "img": "https://ps.ssl.qhimg.com/t029ca7ed1bf2f00bcd.jpg"},
    {"name": "茅崎夕樱", "img": "https://ps.ssl.qhimg.com/t02ad9a01cecbd9845e.jpg"},
    {"name": "御园莓华", "img": "https://ps.ssl.qhimg.com/t0275f0bc1a598e4811.jpg"},
    {"name": "绫弥 一条", "img": "https://ps.ssl.qhimg.com/t0216758ac7fa9e384a.jpg"},
    {"name": "姬野永远", "img": "https://ps.ssl.qhimg.com/t029caf72d2792c359a.jpg"},
    {"name": "樱小路 露娜", "img": "https://ps.ssl.qhimg.com/t0266561e7bc4cd1100.jpg"},
    {
        "name": "十色煌",
        "img": "https://1.z.wiki/autoupload/20250525/W6ai/1920X1080/%E5%8D%81%E8%89%B2_%E7%85%8C.png",
    },
    {"name": "亚托莉", "img": "https://ps.ssl.qhimg.com/t0200ade6cf7aaa3128.jpg"},
    {"name": "春琉", "img": "https://ps.ssl.qhimg.com/t028239bd7171c8d4f4.jpg"},
    {"name": "茑町千岁", "img": "https://ps.ssl.qhimg.com/t0218f923a81058a05a.jpg"},
    {"name": "此花露 西娅", "img": "https://ps.ssl.qhimg.com/t029339700152fc2615.jpg"},
    {"name": "古倉芽瑠", "img": "https://ps.ssl.qhimg.com/t02279d462b23f01072.jpg"},
    {"name": "黑姫结灯", "img": "https://ps.ssl.qhimg.com/t02176096cd48095334.jpg"},
    {"name": "犬屋恋丸", "img": "https://ps.ssl.qhimg.com/t029d1cf44af6b8c915.jpg"},
    {
        "name": "匂宫巡游",
        "img": "https://cdn.z.wiki/autoupload/20250525/YbS6/1920X1080/%E5%8C%82%E5%AE%AB_%E5%B7%A1%E6%B8%B8.png",
    },
    {"name": "常盘华乃", "img": "https://ps.ssl.qhimg.com/t02f66d10b4558a1454.jpg"},
    {"name": "夏咲咏", "img": "https://ps.ssl.qhimg.com/t0231d13aa486f3e8b6.jpg"},
    {"name": "乙音妮可露", "img": "https://ps.ssl.qhimg.com/t027b58e119077cadf6.jpg"},
    {"name": "不知火祈服", "img": "https://ps.ssl.qhimg.com/t02a6d45499748318d0.jpg"},
    {"name": "朱雀院椿", "img": "https://ps.ssl.qhimg.com/t021e30699f4ad565bd.jpg"},
    {"name": "中津静流", "img": "https://ps.ssl.qhimg.com/t02253c87f485331047.jpg"},
    {"name": "煤谷小夜", "img": "https://ps.ssl.qhimg.com/t0277f167855fe01145.jpg"},
    {"name": "二阶堂真红", "img": "https://ps.ssl.qhimg.com/t022582c3005cfcf032.jpg"},
    {"name": "如月七穗", "img": "https://ps.ssl.qhimg.com/t0281fcceec13c43cd4.jpg"},
    {"name": "英パルヴィ", "img": "https://ps.ssl.qhimg.com/t0244b622267d0685b2.jpg"},
    {"name": "天使酱", "img": "https://ps.ssl.qhimg.com/t02e18691301fa9ea63.jpg"},
    {"name": "一之濑铃夏", "img": "https://ps.ssl.qhimg.com/t02f26d20896b0a1561.jpg"},
    {"name": "夏目历", "img": "https://ps.ssl.qhimg.com/t0245adbf59a0b82b53.jpg"},
    {"name": "锦亚澄", "img": "https://ps.ssl.qhimg.com/t027768ce83de90283d.jpg"},
    {"name": "夜刀 玖玖瑠", "img": "https://ps.ssl.qhimg.com/t0230f19cafd5218fc9.jpg"},
    {"name": "如月 澪", "img": "https://ps.ssl.qhimg.com/t02c72f6a1c34a9923b.jpg"},
    {"name": "琴濑", "img": "https://ps.ssl.qhimg.com/t01fb6fa02490fcf662.jpg"},
    {"name": "丛雨", "img": "https://ps.ssl.qhimg.com/t02ca04c76cf8792f74.jpg"},
    {"name": "橘叶月", "img": "https://ps.ssl.qhimg.com/t02543a1e96c751cfbb.jpg"},
    {"name": "四条凛香", "img": "https://ps.ssl.qhimg.com/t022e47b5c0ac92f3d1.jpg"},
    {"name": "三间坂萤", "img": "https://ps.ssl.qhimg.com/t0223350f22b48dac96.jpg"},
    {"name": "红葉", "img": "https://ps.ssl.qhimg.com/t02d6f7e09d2c3341de.jpg"},
    {"name": "因幡巡", "img": "https://ps.ssl.qhimg.com/t02840a643e2409db2d.jpg"},
    {"name": "科罗娜", "img": "https://ps.ssl.qhimg.com/t02a5f4d5733519eba7.jpg"},
    {"name": "柊春", "img": "https://i.postimg.cc/Jzcpw5ph/image.png"},
    {"name": "妃玲奈", "img": "https://ps.ssl.qhimg.com/t020184c45a9913d772.jpg"},
    {"name": "不知出遠子", "img": "https://ps.ssl.qhimg.com/t0270a96779c050ec97.jpg"},
    {"name": "乙原恋", "img": "https://ps.ssl.qhimg.com/t023b01802b920a0128.jpg"},
    {"name": "莲", "img": "https://ps.ssl.qhimg.com/t025b46ad5c13791d1e.jpg"},
    {"name": "濑名爱理", "img": "https://ps.ssl.qhimg.com/t024f34a11288ee4b26.jpg"},
    {
        "name": "御樱禀",
        "img": "https://2.z.wiki/autoupload/20250525/wuS1/3840X2160/%E5%BE%A1%E6%A8%B1_%E7%A6%80.png",
    },
    {"name": "奏大雅", "img": "https://ps.ssl.qhimg.com/t02ef63496e3e9951f3.jpg"},
    {"name": "冬马和纱", "img": "https://ps.ssl.qhimg.com/t021942798d735d5457.jpg"},
    {"name": "朱雀院 抚子", "img": "https://ps.ssl.qhimg.com/t0296cbbaed04ec89d9.jpg"},
    {"name": "伏见 理央", "img": "https://ps.ssl.qhimg.com/t02fd29a5e5d35d6c7b.jpg"},
    {"name": "紬文德斯", "img": "https://ps.ssl.qhimg.com/t02b4ac45fa5bee9c4b.jpg"},
    {"name": "夜羽真白", "img": "https://i.postimg.cc/1X5mP2CJ/image.png"},
    {
        "name": "地狱谷咲来",
        "img": "https://1.z.wiki/autoupload/20250525/looR/2560X1440/%E5%9C%B0%E7%8B%B1%E8%B0%B7_%E5%92%B2%E6%9D%A5.png",
    },
    {"name": "御城由乃", "img": "https://ps.ssl.qhimg.com/t02dce05e478b618ced.jpg"},
    {"name": "佐久真詩", "img": "https://ps.ssl.qhimg.com/t024b053d16ca83d568.jpg"},
    {"name": "小河坂 千波", "img": "https://ps.ssl.qhimg.com/t02b2947286df20f205.jpg"},
    {"name": "汐入玖玖里", "img": "https://ps.ssl.qhimg.com/t025fee4d0282ef22ba.jpg"},
    {"name": "结城希亚", "img": "https://ps.ssl.qhimg.com/t02168154a46f203c9f.jpg"},
    {"name": "凑斗光", "img": "https://ps.ssl.qhimg.com/t02ecaab128f3355df5.jpg"},
    {"name": "天神平阳姬", "img": "https://ps.ssl.qhimg.com/t0262d6bd4edf7febfc.jpg"},
    {"name": "鹰苍杏璃", "img": "https://i.postimg.cc/SK13FrtD/image.png"},
    {"name": "香坂春风", "img": "https://ps.ssl.qhimg.com/t027e528754ffcbefe1.jpg"},
    {"name": "夏目雫", "img": "https://ps.ssl.qhimg.com/t02222a7df55a2085ef.jpg"},
    {"name": "千里朱音", "img": "https://ps.ssl.qhimg.com/t0251eb1583812683d4.jpg"},
    {
        "name": "安妮丽丝",
        "img": "https://2.z.wiki/autoupload/20250525/a7Eq/1920X1080/%E5%AE%89%E5%A6%AE%E4%B8%BD%E4%B8%9D.png",
    },
    {
        "name": "鹰仓杏铃",
        "img": "https://2.z.wiki/autoupload/20250525/OnCa/3832X2144/%E9%B9%B0%E4%BB%93_%E6%9D%8F%E9%93%83.png",
    },
    {"name": "僧间理亚", "img": "https://ps.ssl.qhimg.com/t023b6d63fbc3a4a73a.jpg"},
    {"name": "樱来瑞花", "img": "https://ps.ssl.qhimg.com/t025618633a5691c0b9.jpg"},
    {
        "name": "小黑",
        "img": "https://1.z.wiki/autoupload/20250525/YZc0/5120X2880/%E5%B0%8F%E9%BB%91.png",
    },
    {"name": "南乃爱丽丝", "img": "https://ps.ssl.qhimg.com/t02133171009496cb8b.jpg"},
    {"name": "海野宫子", "img": "https://ps.ssl.qhimg.com/t02355b678e787b593d.jpg"},
    {"name": "天川凑月", "img": "https://ps.ssl.qhimg.com/t024844a75349c301ea.jpg"},
    {"name": "敷岛镜", "img": "https://ps.ssl.qhimg.com/t0266fe449c3aac5257.jpg"},
    {
        "name": "本间心铃",
        "img": "https://1.z.wiki/autoupload/20250525/omt8/3840X2160/%E6%9C%AC%E9%97%B4_%E5%BF%83%E9%93%83.png",
    },
    {"name": "小不动摇", "img": "https://ps.ssl.qhimg.com/t02d21f2f1940e9b4b7.jpg"},
    {
        "name": "柯蕾特·阿纳斯塔西娅",
        "img": "https://ps.ssl.qhimg.com/t02020e27ff4e092488.jpg",
    },
    {"name": "橘落叶", "img": "https://ps.ssl.qhimg.com/t028c274c3ad7afe078.jpg"},
    {"name": "朱雀院 红叶", "img": "https://ps.ssl.qhimg.com/t02043d08b5e4f40d6c.jpg"},
    {"name": "神户小鸟", "img": "https://ps.ssl.qhimg.com/t02072ddf7571993252.jpg"},
    {"name": "内藤舞亚", "img": "https://ps.ssl.qhimg.com/t02117f7124ce263bec.jpg"},
    {"name": "妹口弥生", "img": "https://ps.ssl.qhimg.com/t02ecd7491f01b9ce8c.jpg"},
    {"name": "鹭泽有里咲", "img": "https://ps.ssl.qhimg.com/t021ad477266a8a04c0.jpg"},
    {"name": "小花", "img": "https://ps.ssl.qhimg.com/t027761346da59ba5a2.jpg"},
    {"name": "梅丽尔", "img": "https://ps.ssl.qhimg.com/t02792cee9d6cbb98ea.jpg"},
    {"name": "乾纱凪", "img": "https://ps.ssl.qhimg.com/t0237138040aff7d5fd.jpg"},
    {"name": "篝", "img": "https://ps.ssl.qhimg.com/t024acff6c4b8d629c1.jpg"},
    {"name": "夜月姬织", "img": "https://ps.ssl.qhimg.com/t020502db4ae8b383a7.jpg"},
    {"name": "诗音", "img": "https://ps.ssl.qhimg.com/t0260447d4df76d3518.jpg"},
    {
        "name": "藤杏_千和",
        "img": "https://cdn.z.wiki/autoupload/20250525/lCSs/5120X2880/%E8%97%A4%E6%9D%8F_%E5%8D%83%E5%92%8C.png",
    },
    {"name": "空门 苍", "img": "https://ps.ssl.qhimg.com/t024fc9e0bd259d1d33.jpg"},
    {"name": "八坂爱 乃亚", "img": "https://ps.ssl.qhimg.com/t0268a1027d1398d3cd.jpg"},
    {"name": "天雾夕音", "img": "https://ps.ssl.qhimg.com/t02af1736e35e6b1442.jpg"},
    {
        "name": "卡米娜尔·路·普鲁提亚·索尔特雷吉·希斯雅",
        "img": "https://ps.ssl.qhimg.com/t0213564fe96fcacc59.jpg",
    },
    {
        "name": "百濑美月",
        "img": "https://cdn.z.wiki/autoupload/20250525/IMi2/3840X2160/%E7%99%BE%E6%BF%91%E7%BE%8E%E6%9C%88.png",
    },
    {"name": "百濑辉夜", "img": "https://ps.ssl.qhimg.com/t02b9d7d1e9f695823f.jpg"},
    {
        "name": "信田结爱",
        "img": "https://1.z.wiki/autoupload/20250525/14l2/1920X1080/%E4%BF%A1%E7%94%B0_%E7%BB%93%E7%88%B1.png",
    },
    {"name": "凤千早", "img": "https://ps.ssl.qhimg.com/t021f4fed308037db8a.jpg"},
    {"name": "夏目蓝", "img": "https://ps.ssl.qhimg.com/t02f5ab801d17f3b768.jpg"},
    {"name": "架桥琥珀", "img": "https://ps.ssl.qhimg.com/t02df524a945f7eb670.jpg"},
    {"name": "在原七海", "img": "https://ps.ssl.qhimg.com/t02619cfd55e487ffcc.jpg"},
    {"name": "枣铃", "img": "https://ps.ssl.qhimg.com/t020c3a9f257f4b605d.jpg"},
    {
        "name": "GINKA",
        "img": "https://cdn.z.wiki/autoupload/20250525/6gxo/5120X2880/GINKA.png",
    },
    {"name": "野村美希", "img": "https://ps.ssl.qhimg.com/t02ce4cfbab4143379c.jpg"},
    {"name": "夕凪一夏", "img": "https://ps.ssl.qhimg.com/t02074703a05ad8fee5.jpg"},
    {"name": "箱鸟理世", "img": "https://ps.ssl.qhimg.com/t0227bc3d5995577800.jpg"},
    {"name": "水织静久", "img": "https://ps.ssl.qhimg.com/t02507a28672f5ec9c4.jpg"},
    {"name": "库特", "img": "https://ps.ssl.qhimg.com/t02a4c3c496ad5564a6.jpg"},
    {"name": "月社妃", "img": "https://ps.ssl.qhimg.com/t020d79aff6a774f896.jpg"},
    {"name": "新海天", "img": "https://ps.ssl.qhimg.com/t02569373c56c017820.jpg"},
    {"name": "鸣濑白羽", "img": "https://ps.ssl.qhimg.com/t02e3304b1525641f99.jpg"},
    {
        "name": "御子柴瑠衣",
        "img": "https://i.postimg.cc/0NBdRPTK/21ffaa9ff74fb89b7bf7668a7600d912-720.jpg",
    },
    {"name": "久慈恋花", "img": "https://ps.ssl.qhimg.com/t0265abdcdaaa102003.jpg"},
    {
        "name": "白花",
        "img": "https://cdn.z.wiki/autoupload/20250525/Mw0l/2560X1440/%E7%99%BD%E8%8A%B1.png",
    },
    {"name": "日向彼方", "img": "https://ps.ssl.qhimg.com/t02a3fa6a4abc4cd461.jpg"},
    {
        "name": "梅尔·艾什礼佩克",
        "img": "https://ps.ssl.qhimg.com/t023197a724a4a05e13.jpg",
    },
    {"name": "仓科明日香", "img": "https://ps.ssl.qhimg.com/t028d5e410146080748.jpg"},
    {"name": "大垣日向", "img": "https://ps.ssl.qhimg.com/t021980c5fe8be5d0c6.jpg"},
    {"name": "三司绫濑", "img": "https://ps.ssl.qhimg.com/t0224bf96c6c6b08da5.jpg"},
    {"name": "折原冰狐", "img": "https://ps.ssl.qhimg.com/t0258b8374ca373d54e.jpg"},
    {"name": "仓贺野圣良", "img": "https://ps.ssl.qhimg.com/t02001f0498b2f75ae0.jpg"},
    {
        "name": "尤斯蒂娅·阿斯特莉亚",
        "img": "https://ps.ssl.qhimg.com/t02b38fdf5e8d64c7f8.jpg",
    },
    {
        "name": "爱莉安娜_哈特贝尔",
        "img": "https://ps.ssl.qhimg.com/t02fe9c381f80427840.jpg",
    },
    {"name": "白羽 幸", "img": "https://ps.ssl.qhimg.com/t02522fd845007f4edc.jpg"},
    {"name": "冰见山玲", "img": "https://ps.ssl.qhimg.com/t02660ed0a18173f193.jpg"},
    {
        "name": "梅娅·S·艾菲梅拉尔",
        "img": "https://ps.ssl.qhimg.com/t02a1ac7b76fbc00a53.jpg",
    },
    {"name": "九条都[die]", "img": "https://ps.ssl.qhimg.com/t026198bd146e9da9e9.jpg"},
    {"name": "和泉妃爱", "img": "https://ps.ssl.qhimg.com/t0219ac4f7f5f81fdae.jpg"},
    {"name": "天羽 美羽", "img": "https://ps.ssl.qhimg.com/t02b7d07dab07e60581.jpg"},
    {
        "name": "名濑由佳奈",
        "img": "https://1.z.wiki/autoupload/20250525/eIL4/3441X4096/%E5%90%8D%E6%BF%91%E7%94%B1%E4%BD%B3%E5%A5%88.png",
    },
    {"name": "凤米卡", "img": "https://ps.ssl.qhimg.com/t02b4f2adbfdc58f0ee.jpg"},
    {"name": "梁染 汐音", "img": "https://ps.ssl.qhimg.com/t02bd56cf35b9efc60d.jpg"},
    {
        "name": "希尔维娅·路·库洛丝克劳恩·索尔特雷吉·希斯雅",
        "img": "https://ps.ssl.qhimg.com/t02731606efc7762a9a.jpg",
    },
    {
        "name": "观波加奈",
        "img": "https://2.z.wiki/autoupload/20250525/TZ20/3840X2160/%E8%A7%82%E6%B3%A2_%E5%8A%A0%E5%A5%88.png",
    },
    {"name": "君原结爱", "img": "https://ps.ssl.qhimg.com/t02f327c1600cba0881.jpg"},
    {"name": "舞羽娜娜", "img": "https://ps.ssl.qhimg.com/t02e55dbb5e6a6f8d3b.jpg"},
    {"name": "雪々", "img": "https://ps.ssl.qhimg.com/t0289692e21f26d6d1e.jpg"},
    {
        "name": "夏目蓝",
        "img": "https://cdn.z.wiki/autoupload/20250525/pQst/1920X1080/%E5%A4%8F%E7%9B%AE_%E8%93%9D.png",
    },
    {"name": "姫榊小桃", "img": "https://ps.ssl.qhimg.com/t022c8b1f4d88c83d03.jpg"},
    {"name": "水上由岐", "img": "https://ps.ssl.qhimg.com/t024608bd7c629b2923.jpg"},
]


def download_image(character):
    try:
        name = character["name"]
        img_url = character["img"]

        if "?" in img_url:
            img_url = img_url.split("?")[0]

        # 获取文件扩展名
        extension = os.path.splitext(img_url)[1]
        if not extension:  # 如果没有扩展名，默认使用.jpg
            extension = ".jpg"

        # 防止奇怪的字符
        safe_name = "".join(c for c in name if c not in '<>:"/\\|?*')
        filename = f"{safe_name}{extension}"

        print(f"正在下载: {name} -> {filename}")

        response = requests.get(img_url, stream=True, timeout=30)
        response.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"成功下载: {filename}")
        return True

    except Exception as e:
        print(f"下载 {name} 失败: {str(e)}")
        return False


def main():
    if not os.path.exists("downloaded_images"):
        os.makedirs("downloaded_images")

    os.chdir("downloaded_images")

    print("开始下载图片...")

    successful = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_char = {
            executor.submit(download_image, char): char for char in characters
        }

        for future in as_completed(future_to_char):
            char = future_to_char[future]
            try:
                if future.result():
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"处理 {char['name']} 时发生错误: {str(e)}")
                failed += 1

    print(f"\n下载完成！成功: {successful}, 失败: {failed}")


if __name__ == "__main__":
    main()
