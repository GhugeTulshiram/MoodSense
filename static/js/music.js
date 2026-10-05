// ==========================================
// MOODSENSE MUSIC MODULE - YOUTUBE
// ==========================================


// ==========================================
// GET EMOTION FROM URL
// ==========================================

function getEmotionFromURL() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    return params.get("emotion");
}


// ==========================================
// LOAD RECOMMENDED SONGS
// ==========================================

async function loadRecommendedSongs(emotion) {

    const musicContainer =
        document.getElementById("music-list");

    if (!musicContainer) {

        console.error(
            "Music container not found."
        );

        return;
    }


    // Loading message

    musicContainer.innerHTML = `
        <div class="music-loading">

            <div class="loading-icon">
                🎵
            </div>

            <p>
                Finding music for your
                ${escapeHTML(emotion)}
                mood...
            </p>

        </div>
    `;


    try {

        const response =
            await fetch(
                "/recommend/" +
                encodeURIComponent(emotion)
            );


        const data =
            await response.json();


        // Check response

        if (
            !data.success ||
            !data.songs ||
            data.songs.length === 0
        ) {

            musicContainer.innerHTML = `

                <div class="music-empty">

                    <div class="empty-icon">
                        🎵
                    </div>

                    <h3>
                        No Music Found
                    </h3>

                    <p>
                        We could not find music
                        for this mood.
                    </p>

                </div>

            `;

            return;
        }


        // Clear loading message

        musicContainer.innerHTML = "";


        // Create music cards

        data.songs.forEach(
            function(song) {

                const songCard =
                    createSongCard(song);

                musicContainer.appendChild(
                    songCard
                );

            }
        );


    } catch (error) {

        console.error(
            "YouTube Music Error:",
            error
        );


        musicContainer.innerHTML = `

            <div class="music-error">

                <div class="error-icon">
                    ⚠️
                </div>

                <h3>
                    Music Service Unavailable
                </h3>

                <p>
                    Please check your
                    YouTube API configuration.
                </p>

            </div>

        `;
    }
}


// ==========================================
// CREATE SONG CARD
// ==========================================

function createSongCard(song) {

    const card =
        document.createElement("div");


    card.className =
        "song-card";


    // YouTube thumbnail

    const image =
        song.image
            ? song.image
            : "/static/images/logo.png";


    card.innerHTML = `

        <div class="song-image">

            <img
                src="${image}"
                alt="${escapeHTML(song.name)}"
                loading="lazy"
            >

        </div>


        <div class="song-info">

            <h3>
                ${escapeHTML(song.name)}
            </h3>

            <p>
                ${escapeHTML(song.artist)}
            </p>

            <span>
                YouTube Music
            </span>

        </div>


        <div class="song-action">

            <button
                class="play-song-btn"
                type="button">

                ▶ Watch

            </button>

        </div>

    `;


    // Watch button

    const playButton =
        card.querySelector(
            ".play-song-btn"
        );


    playButton.addEventListener(
        "click",
        function() {

            playSong(song);

        }
    );


    return card;
}


// ==========================================
// PLAY / OPEN YOUTUBE VIDEO
// ==========================================

function playSong(song) {

    if (song.youtube_url) {

        window.open(
            song.youtube_url,
            "_blank"
        );

        return;
    }


    if (song.video_id) {

        window.open(
            "https://www.youtube.com/watch?v=" +
            song.video_id,
            "_blank"
        );

        return;
    }


    alert(
        "YouTube video is not available."
    );
}


// ==========================================
// ESCAPE HTML
// ==========================================

function escapeHTML(value) {

    if (!value) {
        return "";
    }


    const div =
        document.createElement("div");


    div.textContent =
        value;


    return div.innerHTML;
}


// ==========================================
// UPDATE EMOTION DISPLAY
// ==========================================

function updateEmotionDisplay(emotion) {

    const emotionElement =
        document.getElementById(
            "detected-emotion"
        );


    if (!emotionElement) {
        return;
    }


    const emotionIcons = {

        happy: "😊",

        sad: "😢",

        angry: "😠",

        fear: "😨",

        disgust: "🤢",

        surprise: "😲",

        neutral: "😐"

    };


    const icon =
        emotionIcons[
            emotion.toLowerCase()
        ] || "🎵";


    emotionElement.innerHTML = `

        <span class="emotion-icon">
            ${icon}
        </span>

        <span>
            ${escapeHTML(emotion)}
        </span>

    `;
}


// ==========================================
// AUTO LOAD MUSIC
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const emotion =
            getEmotionFromURL();


        if (emotion) {

            updateEmotionDisplay(
                emotion
            );


            loadRecommendedSongs(
                emotion
            );

        }

    }
);