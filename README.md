# EmojisAndWeather

Week 1 (10/24-10/31):
* Build initial web scraper for Twitter
  * Tentatively using Python
  * Determine which emojis will be used
* Build initial web scraper for NOAA
  * Tentatively using Python
  * Determine which cities will be targeted
* Note: May not want to create both scrapers completely separately

Week 2 (10/31-11/7):
* Finalize web scrapers
* Begin data preprocessing
  * Emoji Extraction
    * Represent each day as an emoji vector
  * Isolate days that have clear weather patterns
    * Represent each day as a atmosphere/temperature pair

Week 3 (11/7-11/14):
* Finalize data preprocessing (See Above)

Week 4 (11/14-11/21):
* Build models
  * Model that picks weather patterns we believe are associated with the most common emoji for the given day
    * Tentatively using more Python (numpy and scipy)
  * Gaussian Mixture Model
    * Tentatively using Python (SciKit Learn)
  * Neural Network
    * Tentatively using Python (Keras)
* Begin Training
  * If need more processing power, then setup server for training

Week 5 (11/21-11/28):
* Continue Training models
* Tune parameters
  * Tune Gaussian Mixture Model
  * Tune Neural Network

Week 6 (11/28-12/5):
* Create Report
* Create Presentation
