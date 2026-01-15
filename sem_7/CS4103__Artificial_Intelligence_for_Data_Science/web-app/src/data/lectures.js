export const lectures = [
    {
        id: 42,
        title: "Lecture 42: Neural Network Learning",
        date: "11/3/2025",
        topics: [
            {
                title: "Forward Propagation",
                content: "The process of calculating the output of a neural network by passing the input through the layers."
            },
            {
                title: "Backpropagation Intuition",
                content: "A method to calculate the gradient of the loss function with respect to the weights. It involves propagating the error backward from the output layer to the input layer."
            },
            {
                title: "Gradient Descent Optimization",
                content: "A method to minimize the loss function by iteratively moving in the direction of the steepest descent (negative gradient)."
            },
            {
                title: "Momentum Method",
                content: "Accelerates learning by accumulating a moving average of past gradients. It helps navigate high curvature, small gradients, and noisy gradients. \n\nFormula: v = δv - α∇J(θ)"
            },
            {
                title: "Nesterov Momentum",
                content: "A variant of momentum where the gradient is evaluated after the current velocity is applied (lookahead). \n\nFormula: v = δv - α∇J(θ + δv)"
            },
            {
                title: "Adam (Adaptive Moments)",
                content: "An adaptive learning rate optimization algorithm that combines the advantages of AdaGrad and RMSProp."
            }
        ],
        flashcards: [
            {
                question: "What is the purpose of the Momentum method in optimization?",
                answer: "To accelerate learning by accumulating a moving average of past gradients, helping to navigate high curvature and noisy gradients."
            },
            {
                question: "How does Nesterov Momentum differ from standard Momentum?",
                answer: "Nesterov Momentum evaluates the gradient *after* applying the current velocity (lookahead), whereas standard Momentum evaluates it at the current position."
            },
            {
                question: "What are the four main disadvantages of Neural Networks mentioned?",
                answer: "1. Lack of transparency (Black box)\n2. Computational expense\n3. Need for large datasets\n4. Overfitting"
            },
            {
                question: "What is Backpropagation?",
                answer: "An algorithm to calculate the gradient of the loss function with respect to the weights by propagating the error backward from the output to the input."
            },
            {
                question: "What is the formula for the Momentum update rule?",
                answer: "v = δv - α∇J(θ)\nθ = θ + v\n(Where δ is decay rate, α is learning rate, v is velocity)"
            },
            {
                question: "Why does standard Gradient Descent sometimes slow down?",
                answer: "It can oscillate in directions of high curvature (e.g., steep valley walls) and make slow progress towards the minimum."
            },
            {
                question: "What is the 'lookahead' property of Nesterov Momentum?",
                answer: "It calculates the gradient at the position where the current momentum would take the parameters (θ + δv), rather than the current position (θ)."
            },
            {
                question: "Which optimization algorithm combines AdaGrad and RMSProp?",
                answer: "Adam (Adaptive Moment Estimation)."
            }
        ],
        quiz: [
            {
                question: "Which optimization algorithm evaluates the gradient after applying the current velocity?",
                options: ["SGD", "Standard Momentum", "Nesterov Momentum", "Adam"],
                correctAnswer: "Nesterov Momentum"
            },
            {
                question: "What does the hyperparameter δ represent in the Momentum method?",
                options: ["Learning rate", "Exponential decay of velocity", "Gradient magnitude", "Batch size"],
                correctAnswer: "Exponential decay of velocity"
            },
            {
                question: "Which of the following is NOT a disadvantage of Neural Networks?",
                options: ["Black box nature", "Computational expense", "Feature extraction", "Overfitting"],
                correctAnswer: "Feature extraction"
            },
            {
                question: "In the context of Momentum, what happens if the gradient is small but consistent?",
                options: ["The velocity decreases", "The velocity accumulates and learning accelerates", "The learning rate is reduced", "The algorithm stops"],
                correctAnswer: "The velocity accumulates and learning accelerates"
            },
            {
                question: "What is the primary motivation for using Momentum over standard SGD?",
                options: ["To reduce the number of parameters", "To accelerate convergence and reduce oscillation", "To avoid overfitting", "To increase model transparency"],
                correctAnswer: "To accelerate convergence and reduce oscillation"
            },
            {
                question: "What does 'Adam' stand for in the context of optimization algorithms?",
                options: ["Adaptive Momentum", "Adaptive Moment Estimation", "Advanced Descent Method", "Automated Decay Algorithm"],
                correctAnswer: "Adaptive Moment Estimation"
            }
        ]
    }
];
