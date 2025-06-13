class DataProcessor {
  static filterRelevantData(data) {
    const finalData = {
      timings: {
        total_time: data[data.length - 1]?.time_elapsed || null,
        sections: {
          demographics_start: null,
          demographics_end: null,
          questions_start: null,
          questions_end: null
        },
        per_question: []
      }
    };

    data.forEach((entry, index) => {
      // Demographics
      if (entry.task === "demographics" && entry.response) {
        const demoFields = ["gender", "age_bracket", "education", "ai_familiarity"];
        const demoResponse = {};
        demoFields.forEach(field => {
          if (entry.response[field] !== undefined) {
            demoResponse[field] = entry.response[field];
          }
        });

        if (Object.keys(demoResponse).length > 0) {
          finalData.response = demoResponse;
        }

        if (finalData.timings.sections.demographics_start === null) {
          finalData.timings.sections.demographics_start = entry.time_elapsed;
        }
        finalData.timings.sections.demographics_end = entry.time_elapsed;
      }

      // Image question
      if (entry.task === "response" && entry.trust !== undefined && entry.image_name) {
        finalData[entry.image_name] = {
          trust: entry.trust,
          label: entry.label,
          confidence: entry.confidence,
          correct_response: entry.correct_response,
          trust_correct: entry.correct_trust,              // was trust classification correct?
          label_correct: entry.correct_classification,     // was spam/ham classification correct?
          ai_classification: entry.ai_classification       // Add the classification (SPAM/HAM)
        };

        finalData.timings.per_question.push({
          image: entry.image_name,
          rt: entry.rt,
          time_elapsed: entry.time_elapsed
        });

        if (finalData.timings.sections.questions_start === null) {
          finalData.timings.sections.questions_start = entry.time_elapsed;
        }
        finalData.timings.sections.questions_end = entry.time_elapsed;
      }
    });

    return finalData;
  }
}
