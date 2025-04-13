# The Balance Scale Addition Game.

### This game teaches addition through visual intuition - imagine a balance scale where students need to find numbers that add up to match a target value. When they're close but not quite right, the scale tilts to show them if their sum is too large or too small!

### 🧠 Addition Skill Progression by Age (6–10 Years) (according to ChatGPT)

| Age   | Grade      | Number Range      | Example Problems                                | Key Skills                             |
|-------|------------|-------------------|-------------------------------------------------|----------------------------------------|
| 6–7   | 1st Grade  | Up to 100         | 7 + 8, 23 + 5, 15 + 16                          | Basic facts, intro to regrouping       |
| 7–8   | 2nd Grade  | Up to 1,000       | 57 + 68, 245 + 37, simple word problems         | Regrouping, double-digit comfort       |
| 8–9   | 3rd Grade  | Up to 10,000      | 628 + 347, 4783 + 246, multi-step problems      | Fluency with regrouping, mental math   |
| 9–10  | 4th Grade  | Up to 1,000,000   | 58,739 + 19,246, multi-number column addition   | Place value, large number handling     |

(Let's divide them by 2 for the sake of my sanity)

## Tech Stack
- Required - Vue.js, Firebase Auth, Session Management, Tailwind, Pinia/Vuex, Pydantic
- Maybes - Three.js, Websockets


## Features, Functions and Modules
- Function to genrate game numbers
    1. 1 parameter is passed to the function, like 30
    2. It will return 2 arrays called LHS and RHS, sum of both of those arrays would be = 30(or whatever parameter is given)
    3. LHS and RHS should not be equal, can't have more than 1 same number

- Function to generate options
- Module: Drag and Drop (find a dnd-kit equivalent in Vue)
- Websocket Session:
    - Start a Session
    - Generate a problem
    - wait for answer
    - save the response
    - if right continue to step 2
    - if wrong notify the answer is wrong, wait for correct answer
    - on session end, save progress in DB.

## Frontend Components
- Scale Component
- SignIn/SignOut/SignUp


## Data Schema and Strategy
- idk, we ball on this one

## References
### Existing Games
1. https://toytheater.com/addition-scale/
2. https://toytheater.com/scale/
3. https://www.roomrecess.com/Tools/PanBalance/play.html

### Dev
1. Dnd
    1. https://github.com/SortableJS/Vue.Draggable
    2. https://learnvue.co/articles/vue-drag-and-drop


## Draft 1 (Websocket Logic)
1. Client creates connection 
2. Client Clicks on Start
3. Send message where type is "start" to socket
4. Socket Sends back two arrays
5. Client is shown an 2 arrays and has to input 1 number so that sum of both arrays are equal
6. Client then sends answer to socket
7. Socket evaluates if the answer is correct
8. If right sends success
9. If wrong send fail
10. wait for step 1
