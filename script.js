const form = document.getElementById('uploadForm');
const classImageInput = document.getElementById('class_image');
const presentList = document.getElementById('present-list');
const absentList = document.getElementById('absent-list');
const presentCount = document.getElementById('present-count');
const absentCount = document.getElementById('absent-count');
const resultsDiv = document.getElementById('results');
const progressBarContainer = document.getElementById('progress-bar-container');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');

form.onsubmit = async (e) => {
    e.preventDefault();
    resultsDiv.style.display = 'none';
    presentList.innerHTML = '';
    absentList.innerHTML = '';
    progressBarContainer.style.display = 'block';

    const formData = new FormData();
    formData.append("image", classImageInput.files[0]);

    // Simulate progress updates
    let progress = 0;
    const intervalId = setInterval(() => {
        progress += 10;
        if (progress > 100) {
            progress = 100;
        }
        progressBar.value = progress;
        progressText.textContent = `${progress}%`;
        if (progress === 100) {
            clearInterval(intervalId);
        }
    }, 100);

    const response = await fetch('/upload-attendance', {
        method: 'POST',
        body: formData
    });

    clearInterval(intervalId);
    progressBarContainer.style.display = 'none';

    const data = await response.json();
    const { present_students, absent_students } = data;

    presentCount.innerText = present_students.length;
    absentCount.innerText = absent_students.length;

    for (const student of present_students) {
        const div = document.createElement('div');
        div.className = 'student-card present';
        div.innerHTML = `<img src="/static/faces/${student.roll_number}.png" onerror="this.src='/static/faces/default_face.jpg'"><br>${student.name}`;
        presentList.appendChild(div);
    }

    for (const student of absent_students) {
        const div = document.createElement('div');
        div.className = 'student-card absent';
        div.innerHTML = `<img src="/static/faces/${student.roll_number}.png" onerror="this.src='/static/faces/default_face.jpg'"><br>${student.name}`;
        absentList.appendChild(div);
    }

    resultsDiv.style.display = 'block';
};