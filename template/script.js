// Data for each member, including image URLs
const memberInfo = {
    alex: {
        name: "Alex Smith",
        info: "Alex is President, overseeing the club’s operations, setting strategic goals, and ensuring all members fulfill their responsibilities.",
        image: "images/people/alex-smith.jpeg" 
    },
    haiar: {
        name: "Haiar Isliamov",
        info: "Haiar is Vice President, ensuring all tasks are understood and completed, and facilitates communication among leadership.",
        image: "images/people/haiar-isliamov.jpeg" 
    },
    dennis: {
        name: "Dennis Voloshko",
        info: "Dennis is Treasurer, handling the club’s finances and reaching out for funding opportunities.",
        image: "images/people/dennis-voloshko.jpeg"
    },
    thomas: {
        name: "Thomas Vogeley",
        info: "Thomas is VP of DEI, organizing initiatives to promote diversity in the club’s recruitment and ensuring an inclusive environment.",
        image: "images/people/thomas-vogeley.jpeg" 
    },
    julio: {
        name: "Julio Kutrolli",
        info: "Julio is the VP of Outreach, maintaining relationships with Career Services to bring in alumni guest speakers and manages external club communications, including email.",
        image: "images/people/julio-kutrolli.jpeg" 
    },
    daniel: {
        name: "Daniel Bitensky",
        info: "Daniel is the VP of Events, organizing speaker events, networking sessions, and club activities to enhance member engagement and learning.",
        image: "images/people/daniel-bitensky.jpeg" 
    },
    paul: {
        name: "Paul Iacobucci",
        info: "Paul is the VP of Technology and the Head of Quantitative Finance.",
        image: "images/people/paul-iacobucci.jpg"
    },
    akhil: {
        name: "Akhil Kagithapu",
        info: "Akhil is a Lead of Quantitative Finance, currently designing the portfolio management algorithm for FA25 NME.",
        image: "images/people/akhil-kagithapu.jpg" 
    },
    gabriel: {
        name: "Gabriel Castillo",
        info: "Gabriel is a Lead of Quantitative Finance and Co-Developer of the site.",
        image: "images/people/gabriel-castillo.jpg" 
    },
    james: {
        name: "James Lynch",
        info: "James is VP of Investments, managing the portfolio and making investments based off club voting.",
        image: "images/people/james-lynch.jpg" 
    }
};

// Function to show popup with member details
function showPopup(memberId) {
    console.log("Popup triggered for:", memberId); // Log to console
    const member = memberInfo[memberId];

    if (member) {
        document.getElementById('member-name').innerText = member.name;
        document.getElementById('member-info').innerText = member.info;
        document.getElementById('popup-image').src = member.image;

        // Add class to show the popup
        const popup = document.getElementById('popup');
        popup.classList.add('show'); // Add show class to make it visible
    }
}

// Function to hide popup
function hidePopup() {
    const popup = document.getElementById('popup');
    popup.classList.remove('show'); // Remove class to hide the popup
}


// Bind event listener to close button
document.querySelector('.close-btn').addEventListener('click', hidePopup);

// Optional: Close popup if clicking outside of it
document.addEventListener('click', function(event) {
    const popup = document.getElementById('popup');
    const popupContent = document.querySelector('.popup-content');
    
    // Check if the popup is visible and the click is outside the popup content
    if (popup.style.display === 'flex' && !popupContent.contains(event.target)) {
        hidePopup();
    }
});

//sample member
// member9: {
//     name: "Member 9",
//     info: "Member 9 supports new members with onboarding and resources.",
//     image: "images/filler.png"
// }
