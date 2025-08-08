import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- ✅ TOKEN CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "7010932994:AAFoIqUi6mhosfuFFarrANZmfRffOuz_fdI"
TOGATHER_API_KEY = "6b9170474f79ca06987a8ad12a39c5aeecab90c62ea68eb93f7c60419e0b48fe"

# --- 📚 Syllabus Data (Classes, Subjects, Chapters) ---
CLASS_SUBJECTS = {
    1: ["english", "math", "science", "hindi", "evs"],
    2: ["english", "math", "science", "hindi", "evs"],
    3: ["english", "math", "science", "hindi", "evs"],
    4: ["english", "math", "science", "hindi", "evs"],
    5: ["english", "math", "science", "hindi", "evs"],
    6: ["english", "math", "science", "hindi", "social_science"],
    7: ["english", "math", "science", "hindi", "social_science"],
    8: ["english", "math", "science", "hindi", "social_science"],
    9: ["english", "math", "science", "hindi", "social_science"],
    10: ["english", "math", "science", "hindi", "social_science"],
    11: [
        "english",
        "physics",
        "chemistry",
        "math",
        "biology",
        "hindi",
        "history",
        "geography",
        "political_science",
        "economics",
        "psychology",
        "sociology",
    ],
    12: [
        "english",
        "physics",
        "chemistry",
        "math",
        "biology",
        "hindi",
        "history",
        "geography",
        "political_science",
        "economics",
        "psychology",
        "sociology",
    ],
}

SUBJECT_CHAPTERS = {
    "english": {
        1: [
            "Marigold - Unit 1",
            "Marigold - Unit 2",
            "Marigold - Unit 3",
            "Marigold - Unit 4",
            "Marigold - Unit 5",
            "Marigold - Unit 6",
            "Marigold - Unit 7",
            "Marigold - Unit 8",
            "Marigold - Unit 9",
            "Marigold - Unit 10",
        ],
        2: [
            "Marigold - Unit 1",
            "Marigold - Unit 2",
            "Marigold - Unit 3",
            "Marigold - Unit 4",
            "Marigold - Unit 5",
            "Marigold - Unit 6",
            "Marigold - Unit 7",
            "Marigold - Unit 8",
            "Marigold - Unit 9",
            "Marigold - Unit 10",
        ],
        3: [
            "Marigold - Unit 1",
            "Marigold - Unit 2",
            "Marigold - Unit 3",
            "Marigold - Unit 4",
            "Marigold - Unit 5",
            "Marigold - Unit 6",
            "Marigold - Unit 7",
            "Marigold - Unit 8",
            "Marigold - Unit 9",
            "Marigold - Unit 10",
        ],
        6: [
            "Who Did Patrick's Homework",
            "How the Dog Found Himself",
            "Taro's Reward",
            "An Indian American Woman in Space",
            "A Different Kind of School",
            "Who I Am",
            "Fair Play",
            "A Game of Chance",
            "Desert Animals",
            "The Banyan Tree",
        ],
        7: [
            "Three Questions",
            "A Gift of Chappals",
            "Gopal and the Hilsa Fish",
            "The Ashes That Made Trees Bloom",
            "Quality",
            "Expert Detectives",
            "The Invention of Vita-Wonk",
            "Fire Friend and Foe",
            "A Bicycle in Good Repair",
            "The Story of Cricket",
        ],
        8: [
            "The Best Christmas Present",
            "The Tsunami",
            "Glimpses of the Past",
            "Bepin Choudhury's Lapse of Memory",
            "The Summit Within",
            "This is Jody's Fawn",
            "A Visit to Cambridge",
            "A Short Monsoon Diary",
            "The Great Stone Face I",
            "The Great Stone Face II",
        ],
        9: [
            "The Fun They Had",
            "The Sound of Music",
            "The Little Girl",
            "A Truly Beautiful Mind",
            "The Snake and the Mirror",
            "My Childhood",
            "Reach for the Top",
            "Kathmandu",
            "If I Were You",
            "The Happy Prince",
        ],
        10: [
            "A Letter to God",
            "Nelson Mandela",
            "Two Stories about Flying",
            "From the Diary of Anne Frank",
            "The Hundred Dresses I",
            "The Hundred Dresses II",
            "Glimpses of India",
            "Mijbil the Otter",
            "Madam Rides the Bus",
            "The Sermon at Benares",
        ],
        11: [
            "The Portrait of a Lady",
            "We're Not Afraid to Die",
            "Discovering Tut",
            "Landscape of the Soul",
            "The Ailing Planet",
            "The Browning Version",
            "The Adventure",
            "Silk Road",
            "Father to Son",
            "The Voice of the Rain",
        ],
        12: [
            "The Last Lesson",
            "Lost Spring",
            "Deep Water",
            "The Rattrap",
            "Indigo",
            "Poets and Pancakes",
            "The Interview",
            "Going Places",
            "My Mother at Sixty-six",
            "Keeping Quiet",
        ],
    },
    "math": {
        1: [
            "Shapes and Space",
            "Numbers from One to Nine",
            "Addition",
            "Subtraction",
            "Numbers from Ten to Twenty",
            "Time",
            "Measurement",
            "Money",
            "Data Handling",
        ],
        2: [
            "What is Long, What is Round?",
            "Counting in Groups",
            "How Much Can You Carry?",
            "Counting in Tens",
            "Patterns",
            "Footprints",
            "Jugs and Mugs",
            "Tens and Ones",
            "My Funday",
            "Add our Points",
            "Lines and Lines",
            "Give and Take",
            "The Longest Step",
            "Birds Come, Birds Go",
            "How Many Ponies?",
        ],
        3: [
            "Where to Look From?",
            "Fun With Numbers",
            "Give and Take",
            "Long and Short",
            "Shapes and Designs",
            "Fun With Give and Take",
            "Time Goes On",
            "Who is Heavier?",
            "How Many Times?",
            "Play With Patterns",
            "Jugs and Mugs",
            "Can We Share?",
            "Smart Charts",
            "Rupees and Paise",
        ],
        6: [
            "Knowing Our Numbers",
            "Whole Numbers",
            "Playing with Numbers",
            "Basic Geometrical Ideas",
            "Understanding Elementary Shapes",
            "Integers",
            "Fractions",
            "Decimals",
            "Data Handling",
            "Mensuration",
            "Algebra",
            "Ratio and Proportion",
            "Symmetry",
            "Practical Geometry",
        ],
        7: [
            "Integers",
            "Fractions and Decimals",
            "Data Handling",
            "Simple Equations",
            "Lines and Angles",
            "The Triangle and its Properties",
            "Congruence of Triangles",
            "Comparing Quantities",
            "Rational Numbers",
            "Practical Geometry",
            "Perimeter and Area",
            "Algebraic Expressions",
            "Exponents and Powers",
            "Symmetry",
        ],
        8: [
            "Rational Numbers",
            "Linear Equations in One Variable",
            "Understanding Quadrilaterals",
            "Practical Geometry",
            "Data Handling",
            "Squares and Square Roots",
            "Cubes and Cube Roots",
            "Comparing Quantities",
            "Algebraic Expressions and Identities",
            "Mensuration",
            "Exponents and Powers",
            "Direct and Inverse Proportions",
            "Factorisation",
            "Introduction to Graphs",
        ],
        9: [
            "Number Systems",
            "Polynomials",
            "Coordinate Geometry",
            "Linear Equations in Two Variables",
            "Introduction to Euclid's Geometry",
            "Lines and Angles",
            "Triangles",
            "Quadrilaterals",
            "Areas of Parallelograms and Triangles",
            "Circles",
            "Constructions",
            "Heron's Formula",
            "Surface Areas and Volumes",
            "Statistics",
            "Probability",
        ],
        10: [
            "Real Numbers",
            "Polynomials",
            "Pair of Linear Equations in Two Variables",
            "Quadratic Equations",
            "Arithmetic Progressions",
            "Triangles",
            "Coordinate Geometry",
            "Introduction to Trigonometry",
            "Some Applications of Trigonometry",
            "Circles",
            "Constructions",
            "Areas Related to Circles",
            "Surface Areas and Volumes",
            "Statistics",
            "Probability",
        ],
        11: [
            "Sets",
            "Relations and Functions",
            "Trigonometric Functions",
            "Mathematical Induction",
            "Complex Numbers",
            "Linear Inequalities",
            "Permutations and Combinations",
            "Binomial Theorem",
            "Sequences and Series",
            "Straight Lines",
            "Conic Sections",
            "Introduction to Three Dimensional Geometry",
            "Limits and Derivatives",
            "Mathematical Reasoning",
            "Statistics",
            "Probability",
        ],
        12: [
            "Relations and Functions",
            "Inverse Trigonometric Functions",
            "Matrices",
            "Determinants",
            "Continuity and Differentiability",
            "Applications of Derivatives",
            "Integrals",
            "Applications of Integrals",
            "Differential Equations",
            "Vector Algebra",
            "Three Dimensional Geometry",
            "Linear Programming",
            "Probability",
        ],
    },
    "science": {
        1: [
            "Plants Around Us",
            "Animals Around Us",
            "My Body",
            "Food and Water",
            "Shelter",
            "Things Around Us",
        ],
        2: [
            "Living and Non-living Things",
            "Plants",
            "Animals",
            "Our Body",
            "Food",
            "Materials and Objects",
            "Water",
            "Air Around Us",
            "Weather and Sky",
        ],
        3: [
            "Plants Around Us",
            "Animals Around Us",
            "My Body",
            "Food We Eat",
            "Water",
            "Air Around Us",
            "Our Environment",
            "Occupation and Services",
            "Transport and Communication",
            "Safety and First Aid",
        ],
        6: [
            "Food - Where Does it Come From",
            "Components of Food",
            "Fibre to Fabric",
            "Sorting Materials into Groups",
            "Separation of Substances",
            "Changes Around Us",
            "Getting to Know Plants",
            "Body Movements",
            "The Living Organisms",
            "Motion and Measurement of Distances",
            "Light, Shadows and Reflections",
            "Electricity and Circuits",
            "Fun with Magnets",
            "Water",
            "Air Around Us",
            "Garbage In, Garbage Out",
        ],
        7: [
            "Nutrition in Plants",
            "Nutrition in Animals",
            "Fibre to Fabric",
            "Heat",
            "Acids, Bases and Salts",
            "Physical and Chemical Changes",
            "Weather, Climate and Adaptations",
            "Winds, Storms and Cyclones",
            "Soil",
            "Respiration in Organisms",
            "Transportation in Animals and Plants",
            "Reproduction in Plants",
            "Motion and Time",
            "Electric Current and its Effects",
            "Light",
            "Water: A Precious Resource",
            "Forests: Our Lifeline",
            "Wastewater Story",
        ],
        8: [
            "Crop Production and Management",
            "Microorganisms",
            "Synthetic Fibres and Plastics",
            "Materials: Metals and Non-Metals",
            "Coal and Petroleum",
            "Combustion and Flame",
            "Conservation of Plants and Animals",
            "Cell - Structure and Functions",
            "Reproduction in Animals",
            "Reaching the Age of Adolescence",
            "Force and Pressure",
            "Friction",
            "Sound",
            "Chemical Effects of Electric Current",
            "Some Natural Phenomena",
            "Light",
            "Stars and the Solar System",
            "Pollution of Air and Water",
        ],
        9: [
            "Matter in Our Surroundings",
            "Is Matter Around Us Pure",
            "Atoms and Molecules",
            "Structure of the Atom",
            "The Fundamental Unit of Life",
            "Tissues",
            "Diversity in Living Organisms",
            "Motion",
            "Force and Laws of Motion",
            "Gravitation",
            "Work and Energy",
            "Sound",
            "Why Do We Fall Ill",
            "Natural Resources",
            "Improvement in Food Resources",
        ],
        10: [
            "Light - Reflection and Refraction",
            "Human Eye and Colourful World",
            "Electricity",
            "Magnetic Effects of Electric Current",
            "Acids, Bases and Salts",
            "Metals and Non-metals",
            "Carbon and its Compounds",
            "How do Organisms Reproduce",
            "Heredity and Evolution",
            "Light - Reflection and Refraction",
            "Our Environment",
            "Management of Natural Resources",
        ],
        11: [
            "The Living World",
            "Biological Classification",
            "Plant Kingdom",
            "Animal Kingdom",
            "Morphology of Flowering Plants",
            "Anatomy of Flowering Plants",
            "Structural Organisation in Animals",
            "Cell: The Unit of Life",
            "Biomolecules",
            "Cell Cycle and Cell Division",
            "Transport in Plants",
            "Mineral Nutrition",
            "Photosynthesis in Higher Plants",
            "Respiration in Plants",
            "Plant Growth and Development",
            "Digestion and Absorption",
            "Breathing and Exchange of Gases",
            "Body Fluids and Circulation",
            "Excretory Products and their Elimination",
            "Locomotion and Movement",
            "Neural Control and Coordination",
            "Chemical Coordination and Integration",
        ],
        12: [
            "Reproduction in Organisms",
            "Sexual Reproduction in Flowering Plants",
            "Human Reproduction",
            "Reproductive Health",
            "Principles of Inheritance and Variation",
            "Molecular Basis of Inheritance",
            "Evolution",
            "Human Health and Disease",
            "Strategies for Enhancement in Food Production",
            "Microbes in Human Welfare",
            "Biotechnology and its Applications",
            "Biotechnology and its Applications",
            "Organisms and Populations",
            "Ecosystem",
            "Biodiversity and Conservation",
            "Environmental Issues",
        ],
    },
    "physics": {
        11: [
            "Physical World",
            "Units and Measurements",
            "Motion in a Straight Line",
            "Motion in a Plane",
            "Laws of Motion",
            "Work, Energy and Power",
            "System of Particles and Rotational Motion",
            "Gravitation",
            "Mechanical Properties of Solids",
            "Mechanical Properties of Fluids",
            "Thermal Properties of Matter",
            "Thermodynamics",
            "Kinetic Theory",
            "Oscillations",
            "Waves",
        ],
        12: [
            "Electric Charges and Fields",
            "Electrostatic Potential and Capacitance",
            "Current Electricity",
            "Moving Charges and Magnetism",
            "Magnetism and Matter",
            "Electromagnetic Induction",
            "Alternating Current",
            "Electromagnetic Waves",
            "Ray Optics and Optical Instruments",
            "Wave Optics",
            "Dual Nature of Radiation and Matter",
            "Atoms",
            "Nuclei",
            "Semiconductor Electronics",
        ],
    },
    "chemistry": {
        11: [
            "Some Basic Concepts of Chemistry",
            "Structure of Atom",
            "Classification of Elements",
            "Chemical Bonding and Molecular Structure",
            "States of Matter",
            "Thermodynamics",
            "Equilibrium",
            "Redox Reactions",
            "Hydrogen",
            "The s-Block Elements",
            "The p-Block Elements",
            "Organic Chemistry",
            "Hydrocarbons",
            "Environmental Chemistry",
        ],
        12: [
            "The Solid State",
            "Solutions",
            "Electrochemistry",
            "Chemical Kinetics",
            "Surface Chemistry",
            "General Principles and Processes of Isolation of Elements",
            "The p-Block Elements",
            "The d- and f-Block Elements",
            "Coordination Compounds",
            "Haloalkanes and Haloarenes",
            "Alcohols, Phenols and Ethers",
            "Aldehydes, Ketones and Carboxylic Acids",
            "Amines",
            "Biomolecules",
            "Polymers",
            "Chemistry in Everyday Life",
        ],
    },
    "biology": {
        11: [
            "The Living World",
            "Biological Classification",
            "Plant Kingdom",
            "Animal Kingdom",
            "Morphology of Flowering Plants",
            "Anatomy of Flowering Plants",
            "Structural Organisation in Animals",
            "Cell: The Unit of Life",
            "Biomolecules",
            "Cell Cycle and Cell Division",
            "Transport in Plants",
            "Mineral Nutrition",
            "Photosynthesis in Higher Plants",
            "Respiration in Plants",
            "Plant Growth and Development",
            "Digestion and Absorption",
            "Breathing and Exchange of Gases",
            "Body Fluids and Circulation",
            "Excretory Products and their Elimination",
            "Locomotion and Movement",
            "Neural Control and Coordination",
            "Chemical Coordination and Integration",
        ],
        12: [
            "Reproduction in Organisms",
            "Sexual Reproduction in Flowering Plants",
            "Human Reproduction",
            "Reproductive Health",
            "Principles of Inheritance and Variation",
            "Molecular Basis of Inheritance",
            "Evolution",
            "Human Health and Disease",
            "Strategies for Enhancement in Food Production",
            "Microbes in Human Welfare",
            "Biotechnology: Principles and Processes",
            "Biotechnology and its Applications",
            "Organisms and Populations",
            "Ecosystem",
            "Biodiversity and Conservation",
            "Environmental Issues",
        ],
    },
    "hindi": {
        6: [
            "वह चिड़िया जो",
            "बचपन",
            "नादान दोस्त",
            "चाँद से थोड़ी सी गप्पें",
            "अक्षरों का महत्व",
            "पार नज़र के",
            "साथी हाथ बढ़ाना",
            "ऐसे-ऐसे",
            "टिकट एल्बम",
            "झांसी की रानी",
            "जो वीर बने",
            "संसार पुस्तक है",
        ],
        7: [
            "हम पंछी उन्मुक्त गगन के",
            "दादी माँ",
            "हिमालय की बेटियाँ",
            "कठपुतली",
            "मिठाईवाला",
            "रक्त और हमारा शरीर",
            "पापा खो गए",
            "शाम एक किसान",
            "चिड़िया की बच्ची",
            "अपूर्व अनुभव",
            "रहीम के दोहे",
            "कंचा",
            "एक तिनका",
            "खुशबू रचते हैं हाथ",
        ],
        8: [
            "ध्वनि",
            "लाख की चूड़ियाँ",
            "बस की यात्रा",
            "दीवानों की हस्ती",
            "चिट्ठियों की अनूठी दुनिया",
            "भगवान के डाकिए",
            "क्या निराश हुआ जाए",
            "यह सबसे कठिन समय नहीं",
            "कबीर की साखियाँ",
            "कामचोर",
            "जब सिनेमा ने बोलना सीखा",
            "सुदामा चरित",
            "जहाँ पहिया है",
            "अकबरी लोटा",
            "सूर के पद",
            "पानी की कहानी",
            "बाज और साँप",
            "टोपी शुक्ला",
        ],
        9: [
            "दो बैलों की कथा",
            "ल्हासा की ओर",
            "उपभोक्तावाद की संस्कृति",
            "साँवले सपनों की याद",
            "नाना साहब की पुत्री देवी मैना को भस्म कर दिया गया",
            "प्रेमचंद के फटे जूते",
            "मेरे बचपन के दिन",
            "एक कुत्ता और एक मैना",
            "गिल्लू",
            "स्मृति",
            "कल्लू कुम्हार की उंकुति",
            "राम लक्ष्मण परशुराम संवाद",
            "दोहे",
            "ग्राम श्री",
            "चंद्र गहना से लौटती बेर",
            "मेघ आए",
            "वर्षा",
            "बच्चे काम पर जा रहे हैं",
            "अग्नि पथ",
        ],
        10: [
            "सूरदास के पद",
            "तुलसीदास",
            "देव",
            "जयशंकर प्रसाद",
            "सूर्यकांत त्रिपाठी 'निराला'",
            "नागार्जुन",
            "गिरिजा कुमार माथुर",
            "ऋतुराज",
            "मंगलेश डबराल",
            "स्वयं प्रकाश",
            "सर्वेश्वर दयाल सक्सेना",
            "हरिशंकर परसाई",
            "यशपाल",
            "प्रहलाद अग्रवाल",
            "अंतोन चेखव",
            "निदा फाजली",
            "हबीब तनवीर",
            "भदंत आनंद कौसल्यायन",
        ],
        11: [
            "नमक का दरोगा",
            "मियाँ नसीरुद्दीन",
            "अपू के साथ ढाई साल",
            "विदाई-संभाषण",
            "गलता लोहा",
            "स्पीति में बारिश",
            "जूझ",
            "आलो-आँधारि",
            "दूसरे के दुःख से दुखी",
            "कबीर",
            "सूर",
            "तुलसीदास",
            "केशवदास",
            "बिहारी",
            "मतिराम",
            "घनानंद",
            "आलम",
            "देव",
        ],
        12: [
            "हरिशंकर परसाई",
            "फणीश्वरनाथ रेणु",
            "विष्णु खरे",
            "रघुवीर सहाय",
            "गजानन माधव मुक्तिबोध",
            "शमशेर बहादुर सिंह",
            "केदारनाथ अग्रवाल",
            "सुमित्रानंदन पंत",
            "महादेवी वर्मा",
            "सच्चिदानंद हीरानंद वात्स्यायन 'अज्ञेय'",
            "श्रीकांत वर्मा",
            "तुलसीदास",
            "फिराक गोरखपुरी",
            "उमाशंकर जोशी",
            "मुक्तिबोध",
            "शमशेर बहादुर सिंह",
            "रघुवीर सहाय",
            "गजानन माधव मुक्तिबोध",
        ],
    },
    "social_science": {
        6: [
            "What, Where, How and When?",
            "On the Trail of the Earliest People",
            "From Gathering to Growing Food",
            "In the Earliest Cities",
            "What Books and Burials Tell Us",
            "Kingdoms, Kings and an Early Republic",
            "New Questions and Ideas",
            "Ashoka, The Emperor Who Gave Up War",
            "Vital Villages, Thriving Towns",
            "Traders, Kings and Pilgrims",
            "New Empires and Kingdoms",
            "Buildings, Paintings and Books",
            "The Earth in the Solar System",
            "Globe: Latitudes and Longitudes",
            "Motions of the Earth",
            "Maps",
            "Major Domains of the Earth",
            "Our Country - India",
            "India: Climate, Vegetation and Wildlife",
            "Understanding Diversity",
            "Diversity and Discrimination",
            "What is Government?",
            "Key Elements of a Democratic Government",
            "Panchayati Raj",
            "Rural Administration",
            "Urban Administration",
            "Rural Livelihoods",
            "Urban Livelihoods",
        ],
        7: [
            "Tracing Changes Through a Thousand Years",
            "New Kings and Kingdoms",
            "The Delhi Sultans",
            "The Mughal Empire",
            "Rulers and Buildings",
            "Towns, Traders and Craftspersons",
            "Tribes, Nomads and Settled Communities",
            "Devotional Paths to the Divine",
            "The Making of Regional Cultures",
            "Eighteenth-Century Political Formations",
            "Our Environment",
            "Inside Our Earth",
            "Our Changing Earth",
            "Air",
            "Water",
            "Natural Vegetation and Wildlife",
            "Human Environment",
            "Life in the Temperate Grasslands",
            "Life in the Deserts",
            "On Equality",
            "Role of the Government in Health",
            "How the State Government Works",
            "Growing up as Boys and Girls",
            "Women Change the World",
            "Understanding Media",
            "Understanding Advertising",
            "Markets Around Us",
            "A Shirt in the Market",
        ],
        8: [
            "How, When and Where",
            "From Trade to Territory",
            "Ruling the Countryside",
            "Tribals, Dikus and the Vision of a Golden Age",
            "When People Rebel",
            "Weavers, Iron Smelters and Factory Owners",
            "Civilising the 'Native', Educating the Nation",
            "Women, Caste and Reform",
            "The Making of the National Movement",
            "India After Independence",
            "Resources",
            "Land, Soil, Water, Natural Vegetation and Wildlife Resources",
            "Agriculture",
            "Industries",
            "Human Resources",
            "The Indian Constitution",
            "Understanding Secularism",
            "Why Do We Need a Parliament?",
            "Understanding Laws",
            "Social Change and the Police",
            "Understanding Our Criminal Justice System",
            "Understanding Marginalisation",
            "Confronting Marginalisation",
            "Public Facilities",
            "Law and Social Justice",
        ],
        9: [
            "The French Revolution",
            "Socialism in Europe and the Russian Revolution",
            "Nazism and the Rise of Hitler",
            "Forest Society and Colonialism",
            "Pastoralists in the Modern World",
            "Peasants and Farmers",
            "History and Sport",
            "Clothing: A Social History",
            "India - Size and Location",
            "Physical Features of India",
            "Drainage",
            "Climate",
            "Natural Vegetation and Wildlife",
            "Population",
            "What is Democracy? Why Democracy?",
            "Constitutional Design",
            "Electoral Politics",
            "Working of Institutions",
            "Democratic Rights",
            "The Story of Village Palampur",
            "People as Resource",
            "Poverty as a Challenge",
            "Food Security in India",
        ],
        10: [
            "The Rise of Nationalism in Europe",
            "The Nationalist Movement in Indo-China",
            "Nationalism in India",
            "The Making of a Global World",
            "The Age of Industrialisation",
            "Work, Life and Leisure",
            "Print Culture and the Modern World",
            "Novels, Society and History",
            "Resources and Development",
            "Forest and Wildlife Resources",
            "Water Resources",
            "Agriculture",
            "Minerals and Energy Resources",
            "Manufacturing Industries",
            "Lifelines of National Economy",
            "Power-sharing",
            "Federalism",
            "Democracy and Diversity",
            "Gender, Religion and Caste",
            "Popular Struggles and Movements",
            "Political Parties",
            "Outcomes of Democracy",
            "Challenges to Democracy",
            "Development",
            "Sectors of the Indian Economy",
            "Money and Credit",
            "Globalisation and the Indian Economy",
            "Consumer Rights",
        ],
    },
}

# Aliases and pretty names for subjects
SUBJECT_ALIASES = {
    "sst": "social_science",
    "social science": "social_science",
    "social_science": "social_science",
    "social-studies": "social_science",
    "soc": "social_science",
    "mathematics": "math",
    "maths": "math",
}

def _normalize_subject_key(subject_text: str) -> str:
    text = (subject_text or "").strip().lower().replace("-", " ").replace("_", " ")
    text = " ".join(text.split())
    # direct alias
    if text in SUBJECT_ALIASES:
        return SUBJECT_ALIASES[text]
    # collapse spaces to underscore for canonical
    return text.replace(" ", "_")

def _display_subject_name(subject_key: str) -> str:
    # Replace underscores and title-case, and fix common abbreviations
    pretty = subject_key.replace("_", " ").title()
    if subject_key == "sst" or subject_key == "social_science":
        pretty = "Social Science"
    if subject_key == "math":
        pretty = "Math"
    return pretty

def _get_valid_subject_for_grade(grade: int, subject_input: str) -> str | None:
    if grade not in CLASS_SUBJECTS:
        return None
    normalized = _normalize_subject_key(subject_input)
    # direct match
    for subject_key in CLASS_SUBJECTS[grade]:
        if normalized == subject_key:
            return subject_key
    # fuzzy: match by removing underscores and comparing
    stripped = normalized.replace("_", "")
    for subject_key in CLASS_SUBJECTS[grade]:
        if stripped == subject_key.replace("_", ""):
            return subject_key
    return None

def _format_chapters(chapters: list[str]) -> str:
    return "\n".join([f"{i+1}. {title}" for i, title in enumerate(chapters)])

# --- 🧠 AI Answer from Together API ---
def get_answer_from_together(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGATHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.9
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        result = response.json()
        return result["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- 🌐 Translate to Hindi ---
def translate_to_hindi(text):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": "en|hi"}
    try:
        res = requests.get(url, params=params)
        return res.json()['responseData']['translatedText']
    except:
        return "हिंदी अनुवाद उपलब्ध नहीं है।"

# --- ✅ /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Ask me any Class question in English or Hindi.\n"
        "I’ll reply in both languages (English + हिंदी).\n\n"
        "Use:\n"
        "• /subjects <class> — list subjects (e.g., /subjects 12)\n"
        "• /syllabus <class> <subject> — list chapters (e.g., /syllabus 12 physics)"
    )

# --- 📘 /subjects Command ---
async def subjects_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args or []
    if not args:
        await update.message.reply_text(
            "Usage: /subjects <class>\nExample: /subjects 10"
        )
        return
    try:
        grade = int(args[0])
    except ValueError:
        await update.message.reply_text("Please provide a valid class number. Example: /subjects 9")
        return
    if grade not in CLASS_SUBJECTS:
        await update.message.reply_text("Unsupported class. Available: " + ", ".join(map(str, sorted(CLASS_SUBJECTS.keys()))))
        return
    subjects = CLASS_SUBJECTS[grade]
    pretty_list = ", ".join(_display_subject_name(s) for s in subjects)

    # Inline keyboard for quick syllabus access
    keyboard = []
    row: list[InlineKeyboardButton] = []
    for idx, subject_key in enumerate(subjects):
        text = _display_subject_name(subject_key)
        callback = f"syllabus:{grade}:{subject_key}"
        row.append(InlineKeyboardButton(text=text, callback_data=callback))
        if (idx + 1) % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await update.message.reply_text(
        f"Class {grade} subjects:\n{pretty_list}\n\nTap a button to view the syllabus, or use /syllabus {grade} <subject>.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# --- 📗 /syllabus Command ---
async def syllabus_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args or []
    if len(args) < 2:
        await update.message.reply_text(
            "Usage: /syllabus <class> <subject>\n"
            "Examples:\n"
            "• /syllabus 12 physics\n"
            "• /syllabus 10 social science"
        )
        return
    try:
        grade = int(args[0])
    except ValueError:
        await update.message.reply_text("First argument must be a class number. Example: /syllabus 12 physics")
        return
    subject_input = " ".join(args[1:])
    subject_key = _get_valid_subject_for_grade(grade, subject_input)
    if not subject_key:
        if grade in CLASS_SUBJECTS:
            available = ", ".join(_display_subject_name(s) for s in CLASS_SUBJECTS[grade])
            await update.message.reply_text(
                f"Unknown subject for Class {grade}. Try one of: {available}"
            )
        else:
            await update.message.reply_text("Unsupported class. Try /subjects <class> to see options.")
        return
    chapters = SUBJECT_CHAPTERS.get(subject_key, {}).get(grade)
    if not chapters:
        await update.message.reply_text(
            f"Syllabus not found for Class {grade} {_display_subject_name(subject_key)}."
        )
        return
    formatted = _format_chapters(chapters)
    await update.message.reply_text(
        f"📚 Class {grade} — {_display_subject_name(subject_key)} Syllabus:\n\n{formatted}"
    )

# --- 🔘 Callback for inline syllabus buttons ---
async def handle_syllabus_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        _, grade_str, subject_key = (query.data or "").split(":", 2)
        grade = int(grade_str)
    except Exception:
        await query.edit_message_text("Invalid selection.")
        return
    chapters = SUBJECT_CHAPTERS.get(subject_key, {}).get(grade)
    if not chapters:
        await query.edit_message_text("Syllabus not found.")
        return
    formatted = _format_chapters(chapters)
    await query.edit_message_text(
        f"📚 Class {grade} — {_display_subject_name(subject_key)} Syllabus:\n\n{formatted}"
    )

# --- ✉️ Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text.strip()
    await update.message.reply_text("🧠 Thinking... please wait...")

    english_ans = get_answer_from_together(question)
    hindi_ans = translate_to_hindi(english_ans)

    final_reply = f"""❓ *Question:* {question}

🇬🇧 *English:*
{english_ans}

🇮🇳 *हिंदी:*
{hindi_ans}
"""
    await update.message.reply_text(final_reply, parse_mode="Markdown")

# --- 🚀 Bot Starter ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subjects", subjects_command))
    app.add_handler(CommandHandler("syllabus", syllabus_command))
    app.add_handler(CallbackQueryHandler(handle_syllabus_callback, pattern=r"^syllabus:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()