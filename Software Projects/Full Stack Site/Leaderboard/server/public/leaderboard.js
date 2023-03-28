const leaderboard = document.getElementById("leaderboardData");
var scored;
async function fetchData(url) {
  response = await fetch(url);
  slidespace = await response.json();
  return JSON.parse(slidespace["team"]);
}

async function fetchScores(url) {
  response = await fetch(url);
  scored = await response.json();
  return JSON.parse(scored["scores"])["topic_3"];
}

async function load() {
  leaderboard.innerHTML = "";
  for (let i = 1; i < 27; i++) {
    slidespace_url = `https://slidespace.icu/api/teams/${i}`;
    score_url = `https://slidespace.icu/api/teams/${i}/scores`;
    let info = await fetchData(slidespace_url);
    let title = info["name"];
    let members = info["members"];
    let scores = await fetchScores(score_url);

    let data = document.createElement("div");
    data.classList.add("leaderboarddata");
    data.innerHTML = `<div
    style="
      background: ghostwhite;
      font-size: 20px;
      padding: 10px;
      border: 1px solid lightgray;
      margin: 10px;
      text-align: center;
    "
    class="leaderboard"
  >
            <p>Idea: ${title}</p>
            <p>Members: ${members}</p>
            <p>Scores: ${scores}</p>
            <h3 style="text-align: left">Comments:</h3>
            <div style="text-align: left" id="comment${i}"></div>
            <form style="text-align: left" id="commentform${i}"><input placeholder="Comment" id="typed${i}" required>
            <button type="submit">Comment</button></form>
          </div><br>`;
    leaderboard.appendChild(data);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  load();
});
