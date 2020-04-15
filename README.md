# Smart Teacher
Browser extension that uses NLP and Machine Learning to automatically generate MCQ based quizzes and smart notes for educational videos in youtube and other ed-tech websites.

# Inspiration
In the midst of COVID-19, the whole world has realised the power of online learning and the impact it can have on millions of students. Be it K-12 or higher education, virtual learning is talk of the town. Although there are plenty of video lectures available online and usage is extravagant, often these lectures can get too long, monotonous and quite frankly, boring! People zone out frequently and lose track of what's going on. They end up rewinding the video and watch again which really is a waste of time.

In this process, there is a lack of feedback; there is no one to test you if you've really understood what you've been listening to. What if there was a mechanism to evaluate the understanding? Also, not every student like to take notes. But all of us need something to refer to before an exam. What if there is someone who can automatically generate notes for you while you concentrate on listening to the lecture in the video?

What it does

# What it does:

We have built a web browser extension that automatically generates a quiz and smart notes for videos in YouTube and other EdTech websites using NLP (Natural Language Processing) and Machine Learning. A user can self-evaluate their understanding by taking the quiz while watching the video. Each question presents the user with an option to move back to the part of the video from where the question was generated. This will help the user in revising the concepts which they weren’t able to understand when they watched the video the first time.

We also generate smart notes and summary for the video. Our smart notes also provide meanings and examples for certain key words in the notes so that a user can easily understand the overall content of the notes. User can also click on any sentence in the notes to navigate to the point in the video from where the concept summarized in the sentence is explained.

# Architecture

![alt text](https://github.com/sumanthreddym/smart_teacher/blob/master/Architecture.png)

# Steps to test the plugin:

1. Download/Clone both the folder SmartTeacherPlugin from the Github Repository.
2. Open Chrome web browser. 
3. In browser's search bar, type chrome://extensions/
4. In the extenstions page, click on 'developer mode' at the top right corner of the page.
5. Click on the 'Load Unpacked' button.
6. Choose the folder SmartTeacherPlugin/
7. After the browser plugin is installed successfully, open youtube.
8. Click on the plugin icon next to the browser's search bar. Click on Enable Smart Quizzer button. 
9. Browse an educational video. The plugin will automatically generate smart quiz and smart notes.

Backend is already deployed on an EC2 instance. You don't have to deploy backend to test the plugin.
