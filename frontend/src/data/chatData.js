export const HISTORY = {
  Today: [
    {
      id: 1,
      title: "Photosynthesis Explained",
      preview:
        "Can you explain how plants make food?",
      active: true,
    },
    {
      id: 2,
      title: "World War II Timeline",
      preview:
        "What were the major events of WW2?",
      active: false,
    },
  ],

  Yesterday: [
    {
      id: 3,
      title: "Quadratic Equations",
      preview:
        "How do I solve x² + 5x + 6 = 0?",
      active: false,
    },
    {
      id: 4,
      title: "Python List Comprehension",
      preview:
        "What's the difference between map() and list comprehension?",
      active: false,
    },
  ],

  Earlier: [
    {
      id: 5,
      title: "French Revolution Causes",
      preview:
        "Why did the French Revolution happen?",
      active: false,
    },
    {
      id: 6,
      title: "Newton's Laws of Motion",
      preview:
        "Explain the three laws of motion",
      active: false,
    },
    {
      id: 7,
      title: "Shakespeare Sonnets",
      preview:
        "Analyze Sonnet 18 for me",
      active: false,
    },
  ],
};

export const INITIAL_MESSAGES = [
  {
    from: "bot",
    time: "2:30 PM",
    text:
      "Hello! I'm your NoteAI Tutor 🎓. I'm here to help you understand any topic. What would you like to learn about today?",
  },

  {
    from: "user",
    time: "2:31 PM",
    text:
      "Can you explain how photosynthesis works?",
  },

  {
    from: "bot",
    time: "2:31 PM",
    html: [
      "Great question! Photosynthesis is the process by which plants convert light energy into chemical energy (food).",

      "Here's how it works in simple steps:",

      {
        bold: "1. Light Absorption 🌞",
      },

      "Chlorophyll in plant leaves absorbs sunlight, mainly red and blue wavelengths.",

      {
        bold: "2. Water Splitting",
      },

      "Water (H₂O) absorbed through roots is split into hydrogen and oxygen. Oxygen is released into the atmosphere.",

      {
        bold: "3. Carbon Dioxide Capture 🌿",
      },

      "CO₂ enters through tiny pores called stomata.",

      {
        bold: "4. Sugar Production",
      },

      "The plant combines hydrogen and carbon dioxide to create glucose.",

      {
        bold: "Overall Equation",
      },

      "6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂",

      "Would you like a diagram or quiz on this topic?",
    ],
  },

  {
    from: "user",
    time: "2:34 PM",
    text:
      "What's the difference between light-dependent and light-independent reactions?",
  },

  {
    from: "bot",
    time: "2:35 PM",
    html: [
      "Excellent follow-up! Photosynthesis has two stages:",

      {
        bold:
          "Light-Dependent Reactions (Thylakoid Membrane)",
      },

      {
        bullet:
          "Require direct sunlight",
      },

      {
        bullet:
          "Split water and release oxygen",
      },

      {
        bullet:
          "Produce ATP and NADPH",
      },

      {
        bullet:
          "Acts like charging a battery",
      },

      {
        bold:
          "Light-Independent Reactions / Calvin Cycle",
      },

      {
        bullet:
          "Do not require direct sunlight",
      },

      {
        bullet:
          "Use ATP and NADPH",
      },

      {
        bullet:
          "Convert CO₂ into glucose",
      },

      {
        bullet:
          "Acts like using the battery charge",
      },

      "Think of it like charging your phone and then using it later.",
    ],
  },
];

export const BOT_REPLIES = [
  "That's a great question! Let me explain it step by step.",

  "Sure! Here's a simple explanation that should make it easier to understand.",

  "Good thinking. This concept connects directly to what we discussed earlier.",

  "Let's break this topic into smaller pieces and build your understanding gradually.",

  "This is a very important exam topic. Here's what you need to remember.",

  "A useful way to think about it is through a real-world example.",

  "Here's a quick revision-friendly summary of that concept.",

  "Excellent question. Let's look at both the theory and practical applications.",

  "I can also generate notes or quiz questions on this topic if you'd like.",

  "Let's compare the two concepts side by side for better understanding.",
];

export const QUICK_REPLIES = [
  "Quiz me on this topic",
  "Generate study notes",
  "Give me a real-world example",
  "Explain it more simply",
  "Create MCQs",
  "Important exam questions",
];