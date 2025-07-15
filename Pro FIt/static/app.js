// // This file contains the JavaScript code for the frontend functionality, including handling user interactions, fetching data from the backend, and rendering bar graphs and training tables.

// document.addEventListener('DOMContentLoaded', () => {
//     const progressContainer = document.getElementById('progress-container');
//     const scheduleContainer = document.getElementById('schedule-container');

//     // Fetch user progress data
//     async function fetchUserProgress() {
//         try {
//             const response = await fetch('/api/progress');
//             const data = await response.json();
//             renderProgressBar(data);
//         } catch (error) {
//             console.error('Error fetching user progress:', error);
//         }
//     }

//     // Render progress bar graph
//     function renderProgressBar(data) {
//         const ctx = document.getElementById('progressChart').getContext('2d');
//         const progressChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: data.labels,
//                 datasets: [{
//                     label: 'Workout Progress',
//                     data: data.values,
//                     backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                     borderColor: 'rgba(75, 192, 192, 1)',
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     }

//     // Fetch workout schedule data
//     async function fetchWorkoutSchedule() {
//         try {
//             const response = await fetch('/api/schedule');
//             const scheduleData = await response.json();
//             renderScheduleTable(scheduleData);
//         } catch (error) {
//             console.error('Error fetching workout schedule:', error);
//         }
//     }

//     // Render workout schedule table
//     function renderScheduleTable(scheduleData) {
//         scheduleData.forEach(workout => {
//             const row = document.createElement('tr');
//             row.innerHTML = `
//                 <td>${workout.date}</td>
//                 <td>${workout.exercise}</td>
//                 <td>${workout.reps}</td>
//                 <td>${workout.sets}</td>
//             `;
//             scheduleContainer.appendChild(row);
//         });
//     }

//     // Initialize the app
//     fetchUserProgress();
//     fetchWorkoutSchedule();
// });