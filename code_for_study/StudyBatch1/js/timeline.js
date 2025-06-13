var jsPsych = initJsPsych({
  show_progress_bar: true,
  auto_update_progress_bar: true,
  on_finish: () => {
    const rawData = jsPsych.data.get().values();
    const filtered = DataProcessor.filterRelevantData(rawData);
    jatos.endStudy(JSON.stringify(filtered));
  }
});

var timeline = [];

var imageCorrectAnswersBatch1 = {
  'images/A1B3C3E3.jpg': { trust: 'No', label: 'SPAM' },
  'images/A3B3C3E1.jpg': { trust: 'No', label: 'HAM' },
  'images/A3B3C1E3.jpg': { trust: 'No', label: 'HAM' },
  'images/A3B2C3E3.jpg': { trust: 'No', label: 'HAM' },
  'images/A2B3C3E1.jpg': { trust: 'No', label: 'SPAM' },
  'images/A2B2C3E3.jpg': { trust: 'Yes', label: 'SPAM' },
  'images/A1B3C3E1.jpg': { trust: 'No', label: 'HAM' },
  'images/A1B3C1E3.jpg': { trust: 'Yes', label: 'SPAM' },
  'images/A1B2C3E3.jpg': { trust: 'Yes', label: 'HAM' },
  'images/A3B1C3E1.jpg': { trust: 'Yes', label: 'SPAM' },
  'images/A2B3C1E3.jpg': { trust: 'Yes', label: 'SPAM' },
  'images/A3B2C1E3.jpg': { trust: 'No', label: 'HAM' },
  'images/A3B2C3E1.jpg': { trust: 'No', label: 'SPAM' },
  'images/A3B1C1E3.jpg': { trust: 'Yes', label: 'SPAM' },
  'images/A2B1C1E3.jpg': { trust: 'Yes', label: 'SPAM' },
  'images/A1B1C3E1.jpg': { trust: 'Yes', label: 'HAM' },
  'images/A2B2C1E3.jpg': { trust: 'Yes', label: 'SPAM' },
  'images/A2B1C3E1.jpg': { trust: 'No', label: 'SPAM' },
  'images/A2B2C3E1.jpg': { trust: 'Yes', label: 'HAM' },
  'images/A1B1C1E3.jpg': { trust: 'Yes', label: 'HAM' },
  'images/A1B2C3E1.jpg': { trust: 'No', label: 'SPAM' },
  'images/A1B2C1E3.jpg': { trust: 'No', label: 'SPAM' }
};

var imageDisplayDuration = 7000;

// Function to shuffle an array randomly
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];  // Swap elements
  }
  return array;
}

// Shuffle the image entries (image paths and correct answers)
let imageEntries = Object.entries(imageCorrectAnswersBatch1);
shuffleArray(imageEntries);

let imagePathsToPreload = imageEntries.map(entry => entry[0]);

let trainingImgPaths = [
  'training_images/FeatureCon_words.jpg', 
  'training_images/FeatureImp2_words.jpg',
  'training_images/NoGraph.jpg',
  'training_images/Timed1_words.jpg',
  'training_images/Timed2_noGraph.jpg',
];

imagePathsToPreload = imagePathsToPreload.concat(trainingImgPaths);

// Preload the images
timeline.push({
  type: jsPsychPreload,
  images: imagePathsToPreload
});

// Add timeline items
timeline.push(welcome());
timeline.push(pleaseFillDemo());
timeline.push(demographicSurvey());

//Non-timed training
timeline.push(instructionsBeforeTraining());
timeline.push(displayImageUntilNextWithGuideContribution('training_images/FeatureCon_words.jpg'));
timeline.push(trainingQuestion());

timeline.push(displayImageUntilNextWithGuideImportance('training_images/FeatureImp2_words.jpg'));
timeline.push(trainingQuestion());

timeline.push(displayImageUntilNextWithGuideNoGraph('training_images/NoGraph.jpg'));
timeline.push(trainingQuestion());

//Timed training
timeline.push(instructionsBeforeTimedTraining());
timeline.push(displayImage('training_images/Timed1_words.jpg', imageDisplayDuration));
timeline.push(trainingQuestion());

timeline.push(displayImage('training_images/Timed2_noGraph.jpg', imageDisplayDuration));
timeline.push(trainingQuestion());

timeline.push(instructionsBeforeSurvey());

// Add image and question pairs to the timeline
imageEntries.forEach(([imagePath, answerData]) => {
  const imageName = imagePath.split('/').pop().split('.')[0];
  timeline.push(displayImage(imagePath, imageDisplayDuration));
  timeline.push(question(answerData, imageName));
});

jatos.onLoad(() => {
  jsPsych.run(timeline);
});
