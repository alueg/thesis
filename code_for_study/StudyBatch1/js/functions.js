function displayImage(imagePath, duration) {
  return {
    type: jsPsychImageKeyboardResponse,
    stimulus: imagePath,
    choices: 'NO_KEYS',
    trial_duration: duration,
    stimulus_height: window.innerHeight * 0.8, // scale to 80% of screen height
    data: {
      task: 'image_display',
      image_name: imagePath.split('/').pop().split('.')[0]
    }
  };
}

function welcome() {
  return {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: "Welcome! Press any key to begin.",
    data: { task: "welcome" }
  };
}

function pleaseFillDemo() {
  return {
    type: jsPsychInstructions,
    pages: [
      "Please start by filling out your information. Click 'Next' to continue."
    ],
    show_clickable_nav: true,
    data: { task: "demographic_prompt" }
  };
}

function instructionsBeforeTraining() {
  return {
    type: jsPsychInstructions,
    pages: [
      'In this task, you will see the output of an AI model that has classified an SMS message as either spam or not spam.<br><br>' +
      'You will not see the actual SMS message.<br><br>' +
      'Instead, you will see the model’s classification along with an explanation of why it made that decision.',
      'First, you will be shown some training images.<br><br>' +
      'These images will remain visible until you click "Next" to continue.',
      'After each trial, you will be asked to answer three questions:<br><br>' +
      '1. What was the classification of the SMS?<br><br>' +
      '2. Do you trust this classification?<br><br>' +
      '3. How confident are you in your answer, on a scale from 1 (not confident) to 5 (very confident)?',
      'Click "Next" to begin viewing the training images.'
    ],
    show_clickable_nav: true,
    data: { task: "instructions_before_training" }
  };
}

function instructionsBeforeTimedTraining() {
  return {
    type: jsPsychInstructions,
    pages: [
      'Now that you have seen the static training images, you will move on to the timed training trials.<br><br>' +
      'In these trials, the model’s classification and explanation will be shown for 7 seconds before disappearing automatically.',
      'After each trial, you will again be asked to answer three questions:<br><br>' +
      '1. What was the classification of the SMS?<br><br>' +
      '2. Do you trust this classification?<br><br>' +
      '3. How confident are you in your answer, on a scale from 1 (not confident) to 5 (very confident)?',
      'The process for the timed trials is the same as in the main survey.<br><br>' +
      'Click "Next" to begin the timed trials.'
    ],
    show_clickable_nav: true,
    data: { task: "instructions_before_timed_training" }
  };
}

function instructionsBeforeSurvey() {
  return {
    type: jsPsychInstructions,
    pages: [
      'You have now completed the training trials.<br><br>' +
      'You are about to begin the main survey, where the model’s classification and explanation will be shown for 7 seconds before disappearing.<br><br>' +
      'You will be presented with different types of explanations.',
      'After each trial, you will answer the same three questions:<br><br>' +
      '1. What was the classification?<br><br>' +
      '2. Do you trust this classification?<br><br>' +
      '3. How confident are you in your answer, on a scale from 1 (not confident) to 5 (very confident)?<br><br>' +
      'Click "Next" to begin the survey.'
    ],
    show_clickable_nav: true,
    data: { task: "instructions_before_survey" }
  };
}


function question(correctAnswerObj, imageName) {
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
      image_name: imageName,
      correct_response: correctAnswerObj.trust,  // Expected trust answer
      correct_label: correctAnswerObj.label,     // "SPAM" or "HAM"
      task: 'response'
    },
    on_finish: function (data) {
      const response = data.response;
    
      // Map participant's Likert index to classification string
      const classification = response.ai_classification === 0 ? 'SPAM' : 'HAM';
      const trust = response.trust === 1 ? 'Yes' : 'No';
      const confidence = response.confidence + 1;
    
      // Evaluate correctness
      const correctClassification = (classification === data.correct_label);
      const correctTrust = (trust === data.correct_response);
    
      // Store processed results
      data.ai_classification = classification;  
      data.trust = trust;
      data.confidence = confidence;
      data.correct_classification = correctClassification;
      data.correct_trust = correctTrust;
    
    }
  };
}

function goodbye() {
  return {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: "Thank you for your participation.<br><br>" +
      "Please press any key to end the study.",
    data: { task: "goodbye" }
  };
}
