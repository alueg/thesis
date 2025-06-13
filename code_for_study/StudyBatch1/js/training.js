function trainingQuestion() {
  return {
    type: jsPsychSurveyLikert,
    questions: [
      {
        prompt: "What classification did the AI model assign to the SMS?",
        name: "ai_classification",
        labels: ["Spam", "Not spam"],
        required: true
      },
      {
        prompt: "Do you trust this classification?",
        name: "trust",
        labels: ["No", "Yes"],
        required: true
      },
      {
        prompt: "How confident are you in your answer?",
        name: "confidence",
        labels: [
          "1 <br>Not confident",
          "2",
          "3",
          "4",
          "5 <br>Very confident"
        ],
        required: true
      }
    ],
    data: {
      task: 'training_response'
    }
  };
}

function displayImageUntilNextWithGuideContribution(imagePath) {
  return {
    type: jsPsychHtmlButtonResponse,
    stimulus: `
      <div style="text-align: center;">
        <div style="display: inline-block; max-width: 80%; text-align: left;">
          <img src="${imagePath}" style="max-width: 80%; height: auto; display: block; margin: 0 auto;">
          <br><br>
          <div style="max-width: 80%; font-size: 18px; font-family: Arial, sans-serif; color: #333; margin: 0 auto;">
            <p>
              <strong>Feature Contribution Graph:</strong><br>
              This graph shows how much each word influenced the model’s decision.<br>
              Longer bars indicate a stronger influence.<br>
              <span style="color: #D41159;">Red bars</span> indicate words that pushed the decision toward "spam." <br>
              <span style="color: #1A85FF;">Blue bars</span> indicate words that pushed the decision toward "not spam."
            </p>
            <p>
              <strong>Confidence Score:</strong><br>
              This score reflects how certain the model is about its classification. A higher score indicates greater confidence.
            </p>
            <p>
              <strong>Model's Reasoning:</strong><br>
              This explanation summarizes why the model made its classification.
            </p>
          </div>
        </div>
      </div>
    `,
    choices: ['Next'],
    button_html: ['<button class="jspsych-btn">%choice%</button>'],
    data: {
      task: 'image_until_next_with_guide'
    }
  };
}

function displayImageUntilNextWithGuideImportance(imagePath) {
  return {
    type: jsPsychHtmlButtonResponse,
    stimulus: `
      <div style="text-align: center;">
        <div style="display: inline-block; max-width: 80%; text-align: left;">
          <img src="${imagePath}" style="max-width: 80%; height: auto; display: block; margin: 0 auto;">
          <br><br>
          <div style="max-width: 80%; font-size: 18px; font-family: Arial, sans-serif; color: #333; margin: 0 auto;">
            <p>
              <strong>Feature Importance Graph:</strong><br>
              This graph shows how important each word was in the model’s decision.<br>
              Longer bars represent more influential features.<br>
              <span style="color: #663399;">Purple bars</span> highlight the features the model focused on most.<br>
              Unlike the contribution graph, this shows only importance, not the direction of influence.
            </p>
            <p>
              <strong>Confidence Score:</strong><br>
              This score reflects how certain the model is about its classification. A higher score indicates greater confidence.
            </p>
          </div>
        </div>
      </div>
    `,
    choices: ['Next'],
    button_html: ['<button class="jspsych-btn">%choice%</button>'],
    data: {
      task: 'image_until_next_with_guide'
    }
  };
}

function displayImageUntilNextWithGuideNoGraph(imagePath) {
  return {
    type: jsPsychHtmlButtonResponse,
    stimulus: `
      <div style="text-align: center;">
        <div style="display: inline-block; max-width: 80%; text-align: left;">
          <img src="${imagePath}" style="max-width: 80%; height: auto; display: block; margin: 0 auto;">
          <br><br>
          <div style="max-width: 80%; font-size: 18px; font-family: Arial, sans-serif; color: #333; margin: 0 auto;">
            <p>
              <strong>Confidence Score:</strong><br>
              This score reflects how certain the model is about its classification. A higher score indicates greater confidence.
            </p>
            <p>
              <strong>Model's Reasoning:</strong><br>
              This explanation summarizes why the model made its classification.
            </p>
          </div>
        </div>
      </div>
    `,
    choices: ['Next'],
    button_html: ['<button class="jspsych-btn">%choice%</button>'],
    data: {
      task: 'image_until_next_with_guide'
    }
  };
}
