function demographicSurvey() {
  return {
    type: jsPsychSurveyHtmlForm,
    preamble: "<p>Please fill out the following information.</p>",
    html: `
      <p>
        <label for="gender">Gender:</label><br>
        <select name="gender" id="gender" required>
          <option value="" disabled selected>Select your gender</option>
          <option value="female">Female</option>
          <option value="male">Male</option>
          <option value="non_binary">Non-binary / Third gender</option>
          <option value="prefer_not_say">Prefer not to say</option>
          <option value="other">Other</option>
        </select>
      </p>

      <p>
        <label for="age_bracket">Age:</label><br>
        <select name="age_bracket" id="age_bracket" required>
          <option value="" disabled selected>Select your age range</option>
          <option value="under_18">Under 18</option>
          <option value="18_24">18–24</option>
          <option value="25_34">25–34</option>
          <option value="35_44">35–44</option>
          <option value="45_54">45–54</option>
          <option value="55_64">55–64</option>
          <option value="65_plus">65 or older</option>
        </select>
      </p>

      <p>
        <label for="education">Highest Completed Level of Education:</label><br>
        <select name="education" id="education" required>
          <option value="" disabled selected>Select your highest level</option>
          <option value="less_than_high_school">Less than high school</option>
          <option value="high_school_diploma">High school diploma or equivalent</option>
          <option value="some_college">Some college, no degree</option>
          <option value="bachelor">Bachelor's degree</option>
          <option value="master">Master's degree</option>
          <option value="doctoral">Doctoral or professional degree</option>
          <option value="other">Other</option>
        </select>
      </p>

      <p>
        <label for="ai_familiarity">Familiarity with AI:</label><br>
        <select name="ai_familiarity" id="ai_familiarity" required>
          <option value="" disabled selected>Choose one</option>
          <option value="none">Not at all familiar</option>
          <option value="basic">Basic understanding</option>
          <option value="moderate">Moderate familiarity</option>
          <option value="high">Very familiar / work with AI</option>
        </select>
      </p>
    `,
    data: {
      task: 'demographics'
    }
  };
}