## Inspiration  
Upon inspection of the AWS API it was immediately clear that its computer vision and natural language processing capabilities would be ideal in the context of higher education. Professors across universities lack a concrete way of receiving feedback. The only chance for any kind of feedback is end of semester questionnaires. This method is slow, time-consuming and most importantly inefficient. We wanted to create an app that would allow professors to understand how their students are engaging with their course and make necessary changes not a year after they received the feedback but the very next moment. So, we created Student Reax.

## What it does  
Student Reax offers two tools based on the AWS API. The first one collects and compiles the results of student surveys to draw up a summary pie chart detailing the impressions of the students on the course. To do this we took advantage of AWS's comprehend service to analyze student feedback and assign a positive, negative or neutral score. Our second tool involved using AWS's rekognition service to monitor students' facial features throughout a lecture to determine their engagement. If the AWS API were to be extended to detect more emotions and we were to receive the help of trained psychologists we could then draw up an accurate algorithm that analyzes the students' faces and determines their level of engagement. For the time being our program simply measure the levels of average happiness and calmness of the class as a broad measure of engagement. The results are graphed real-time against time. The tool also returns a live video feed that identifies the students' faces and displays their mood.

## How we built it  
To built it we took advantage of AWS's APIs. Specifically, we used the comprehend and rekognition services. These services were then coupled with our python code to produce a simple interface through which professors could quickly and easily access our tools.

## Challenges we ran into  
The most significant challenge we faced as a team was understanding how to implement APIs. All four of us had little to no experience with using APIs before so this whole field was something very foreign to us.

## Accomplishments that we're proud of  
Our biggest accomplishment was not giving up. There were many points throughout this project that the task of understanding and implementing these complex APIs seemed to tough of a challenge. However, we collectively pushed on and arrived at a fully functioning program.

## What we learned  
APIs are very useful if you have the time and patience to learn about how to actually use it properly.

## What's next for Student Reax  
The big next step to out application is an easy to use UI. This would allow for us to tailor our tools better to our target audience while also giving us the perfect stepping block to keep expanding the services we provide.
