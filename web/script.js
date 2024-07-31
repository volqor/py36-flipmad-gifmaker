let defaultCardWidth = '130px';
let defaultCardHeight = '210px';
let expandedCardWidth = '130px';
let expandedCardHeight = '195px';

function checkCardSize() {
    const logoContainer = document.getElementById('logo-container');
    const downloadContainer = document.getElementById('download-container');
    const demoArea = document.getElementById('demo-area');
    const cardContainer = document.getElementById('card-container');

    if (logoContainer.style.display === 'none' && downloadContainer.style.display === 'none') {
        demoArea.style.justifyContent = 'center';
        cardContainer.style.width = defaultCardWidth;
        cardContainer.style.height = defaultCardHeight;
    } else {
        demoArea.style.justifyContent = 'space-between';
        cardContainer.style.width = expandedCardWidth;
        cardContainer.style.height = expandedCardHeight;
    }
}

function toggleLogo(show) {
    const logoContainer = document.getElementById('logo-container');
    logoContainer.style.display = show ? 'flex' : 'none';
    checkCardSize();
}

function toggleStores(show) {
    const downloadContainer = document.getElementById('download-container');
    downloadContainer.style.display = show ? 'flex' : 'none';
    checkCardSize();
}

function changeSize(size) {
    const demoArea = document.getElementById('demo-area');
    demoArea.style.width = `${size}px`;
    demoArea.style.height = `${size}px`;
    demoArea.style.borderRadius = `${size / 100}px`;
    demoArea.style.padding = `${size / 20}px`;

    const cardContainer = document.getElementById('card-container');
    cardContainer.style.width = `${size / 3}px`;
    cardContainer.style.height = `${size / 2}px`;
    cardContainer.style.marginTop = `${size / 20}px`;

    const cardFront = document.getElementById('card-front');
    const cardBack = document.getElementById('card-back');
    cardFront.style.fontSize = `${size / 12.5}px`;
    cardBack.style.fontSize = `${size / 12.5}px`;
    cardFront.style.borderRadius = `${size / 33.33}px`;
    cardBack.style.borderRadius = `${size / 33.33}px`;

    const logoContainer = document.getElementById('logo-container');
    logoContainer.style.bottom = `${size / 13.33}px`;
    logoContainer.style.left = `${size / 33.33}px`;

    const logoImage = document.getElementById('logo-image');
    logoImage.style.width = `${size / 7.69}px`;
    logoImage.style.height = `${size / 7.69}px`;

    const logoText = document.getElementById('logo-text');
    logoText.style.fontSize = `${size / 16.67}px`;
    logoText.style.marginLeft = `${size / 33.33}px`;

    const downloadContainer = document.getElementById('download-container');
    downloadContainer.style.bottom = `${size / 15.33}px`;
    downloadContainer.style.right = `${size / 33.33}px`;

    const downloadIcon1 = document.getElementById('download-icon1');
    const downloadIcon2 = document.getElementById('download-icon2');
    const iconSize = Math.min(size / 7, size / 5);
    downloadIcon1.style.height = `${iconSize}px`;
    downloadIcon2.style.height = `${iconSize}px`;

    // Update default and expanded sizes
    defaultCardWidth = `${size * 0.4925}px`;
    defaultCardHeight = `${size * 0.83875}px`;
    expandedCardWidth = `${size * 13 / 30}px`;
    expandedCardHeight = `${size * 13 / 20}px`;

    checkCardSize();
}
