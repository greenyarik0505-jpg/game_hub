METADATA = {
    "id": "sea_battle",
    "title": "🚢 Морський Бій 2",
    "author": "Команда Hub (mors_boy)",
    "category": "Strategy",
    "description": "Легендарна гра 'Морський Бій' у зошиті в клітинку. Грайте проти ШІ, купуйте авіаудари, торпеди, радари та змагайтеся за звання адмірала!",
    "image": "assets/sea_battle.png",
    "tags": ["Морський бій", "ШІ", "Стратегія", "Ретро"]
}

import streamlit as st
import streamlit.components.v1 as components

# Set up page config
st.set_page_config(
    page_title="Морской Бой 2 // Sea Battle 2",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to force the HTML5 iframe to occupy the entire screen viewport
st.markdown("""
<style>
/* Hide parent Streamlit layout decoration, headers, and scrollbars */
header {visibility: hidden;}
footer {visibility: hidden;}
div[data-testid="stDecoration"] {display: none;}
.block-container {
    padding: 0px !important;
    max-width: 100% !important;
}
.stApp {
    overflow: hidden !important;
}

/* Make the iframe occupy exactly 100% of the viewport */
iframe {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 999999 !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# HTML5/CSS3/JavaScript Game Code
html_code = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Морской Бой 2</title>
    <link href="https://fonts.googleapis.com/css2?family=Neucha&display=swap" rel="stylesheet">
    <style>
        /* Base notebook styling */
        * {
            box-sizing: border-box;
            font-family: 'Neucha', cursive;
            user-select: none;
            -webkit-user-select: none;
        }

        body {
            background-color: #FAF8F2;
            background-image: 
                linear-gradient(rgba(43, 62, 144, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(43, 62, 144, 0.1) 1px, transparent 1px);
            background-size: 28px 28px;
            background-position: center;
            margin: 0;
            padding: 15px;
            color: #2B3E90;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Doodles on notebook margins */
        .doodle-anchor {
            position: absolute;
            left: 20px;
            top: 100px;
            width: 80px;
            opacity: 0.12;
            pointer-events: none;
        }
        .doodle-plane {
            position: absolute;
            right: 30px;
            top: 80px;
            width: 90px;
            opacity: 0.1;
            pointer-events: none;
        }
        .doodle-sub {
            position: absolute;
            left: 30px;
            bottom: 40px;
            width: 100px;
            opacity: 0.1;
            pointer-events: none;
        }

        /* Container Layout */
        .game-window {
            width: 100%;
            max-width: 1200px;
            height: 100%;
            border: 3px solid #2B3E90;
            border-radius: 8px;
            box-shadow: 8px 8px 0px rgba(43, 62, 144, 0.15);
            background-color: #FAF8F2;
            display: flex;
            flex-direction: column;
            position: relative;
            padding: 20px;
            overflow: hidden;
        }

        /* Profiles and Headers */
        .top-profiles {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2.5px solid #2B3E90;
            padding-bottom: 12px;
            margin-bottom: 15px;
            position: relative;
        }
        .red-margin-top {
            position: absolute;
            bottom: -6px;
            left: 0;
            right: 0;
            height: 2px;
            background-color: rgba(220, 38, 38, 0.45);
        }

        .profile-card {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .profile-card.right {
            flex-direction: row-reverse;
            text-align: right;
        }

        .avatar-box {
            width: 65px;
            height: 65px;
            border: 3px solid #2B3E90;
            border-radius: 6px;
            background-color: #F3EFE3;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 38px;
            box-shadow: 3px 3px 0px rgba(43, 62, 144, 0.1);
            transition: all 0.2s ease-in-out;
        }

        .profile-card.active .avatar-box {
            background-color: #FEF08A; /* warm yellow */
            border-color: #D97706;
            box-shadow: 3px 3px 0px rgba(217, 119, 6, 0.2), 0 0 10px rgba(254, 240, 138, 0.5);
            transform: scale(1.08);
        }

        .profile-info {
            line-height: 1.1;
        }
        .profile-rank {
            font-size: 13px;
            color: #5A6A85;
            font-weight: bold;
        }
        .profile-name {
            font-size: 23px;
            font-weight: bold;
        }
        .profile-score {
            font-size: 16px;
            color: #C2410C;
            font-weight: bold;
        }

        .turn-arrow {
            font-size: 44px;
            color: #10B981;
            font-weight: bold;
            text-shadow: 0px 0px 4px rgba(16, 185, 129, 0.4);
            transition: all 0.3s ease;
        }

        /* Main Layout splitting sidebar options and game screen */
        .main-layout {
            display: flex;
            flex: 1;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        .game-sidebar {
            width: 250px;
            border-right: 2px dashed rgba(43, 62, 144, 0.4);
            padding-right: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            overflow-y: auto;
        }
        .sidebar-section-title {
            font-size: 22px;
            font-weight: bold;
            border-bottom: 2px solid #2B3E90;
            padding-bottom: 4px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .sidebar-item {
            display: flex;
            flex-direction: column;
            gap: 5px;
            font-size: 17px;
        }
        .sidebar-select {
            width: 100%;
            border: 2px solid #2B3E90;
            border-radius: 4px;
            padding: 4px 8px;
            background-color: #FAF8F2;
            color: #2B3E90;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        .sidebar-checkbox-label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: bold;
            cursor: pointer;
        }

        .game-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-y: auto;
            padding-left: 20px;
            position: relative;
            height: 100%;
        }

        /* Screen States */
        .screen {
            display: none;
            flex-direction: column;
            align-items: center;
            width: 100%;
            padding: 10px;
        }
        .screen.active {
            display: flex;
        }

        /* Menu Styles */
        .menu-title {
            font-size: 3.2rem;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 5px;
            text-shadow: 3px 3px 0px rgba(43, 62, 144, 0.1);
            letter-spacing: 2px;
            text-align: center;
        }
        .menu-subtitle {
            font-size: 1.3rem;
            color: #5A6A85;
            margin-bottom: 40px;
            text-align: center;
        }
        .menu-buttons {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 100%;
            max-width: 420px;
        }
        .btn {
            background-color: transparent;
            border: 3px solid #2B3E90;
            border-radius: 255px 15px 225px 15px/15px 225px 15px 255px;
            color: #2B3E90;
            font-size: 22px;
            font-weight: bold;
            padding: 10px 20px;
            cursor: pointer;
            transition: all 0.15s ease-in-out;
            box-shadow: 3px 5px 0px rgba(43, 62, 144, 0.15);
            text-align: center;
            width: 100%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .btn:hover {
            background-color: #FEF08A; /* yellow highlight */
            transform: scale(1.02) rotate(-0.5deg);
            box-shadow: 4px 7px 0px rgba(43, 62, 144, 0.2);
        }
        .btn:active {
            transform: scale(0.98);
        }

        /* Arsenal Shop Screen */
        .shop-title {
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 5px;
            text-align: center;
        }
        .shop-budget {
            font-size: 22px;
            font-weight: bold;
            color: #C2410C;
            margin-bottom: 20px;
            border: 2px dashed #C2410C;
            padding: 4px 15px;
            border-radius: 4px;
            background-color: rgba(194, 65, 12, 0.05);
            text-align: center;
        }
        .shop-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            margin-bottom: 25px;
            width: 100%;
        }
        .shop-card {
            border: 2px solid #2B3E90;
            border-radius: 6px;
            padding: 12px;
            width: 160px;
            background-color: rgba(43, 62, 144, 0.02);
            box-shadow: 3px 3px 0px rgba(43, 62, 144, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .shop-card-icon {
            font-size: 32px;
            margin-bottom: 3px;
        }
        .shop-card-name {
            font-size: 17px;
            font-weight: bold;
            margin-bottom: 2px;
        }
        .shop-card-cost {
            font-size: 15px;
            color: #C2410C;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .shop-card-controls {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .shop-btn-circle {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 2px solid #2B3E90;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.1s;
        }
        .shop-btn-circle:hover {
            background-color: #FEF08A;
        }
        .shop-card-qty {
            font-size: 19px;
            font-weight: bold;
            width: 20px;
            text-align: center;
        }

        /* Placement Screen */
        .placement-container {
            display: flex;
            gap: 25px;
            width: 100%;
            justify-content: center;
            align-items: flex-start;
        }
        .placement-controls {
            flex: 1;
            max-width: 360px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            border: 2px dashed #2B3E90;
            padding: 12px;
            border-radius: 6px;
            background-color: rgba(43, 62, 144, 0.02);
        }

        /* Battle Screen Boards Grid */
        .battle-container {
            display: flex;
            width: 100%;
            justify-content: center;
            align-items: center;
        }
        .board-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }
        .board-title-text {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .board-title-text.left { color: #2B3E90; }
        .board-title-text.right { color: #DC2626; }

        /* The grid logic */
        .board-grid-outer {
            display: flex;
            flex-direction: column;
            position: relative;
        }
        .board-letters {
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            width: 25px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            color: #2B3E90;
        }
        .board-grid {
            width: 320px;
            height: 320px;
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            grid-template-rows: repeat(10, 1fr);
            border: 2px solid #2B3E90;
            background-color: transparent;
            position: relative;
        }
        
        /* Custom styled cells */
        .cell {
            border: 0.5px solid rgba(43, 62, 144, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.1s;
        }
        .cell:hover {
            background-color: #FEF08A;
        }
        .cell-miss {
            color: #2B3E90;
            font-size: 24px;
            line-height: 1;
        }
        .cell-hit {
            color: #DC2626;
            background: repeating-linear-gradient(-45deg, rgba(220,38,38,0.08), rgba(220,38,38,0.08) 3px, rgba(220,38,38,0.2) 3px, rgba(220,38,38,0.2) 6px);
        }
        .cell-sunk {
            color: #EF4444;
            background-color: rgba(220, 38, 38, 0.12);
            border: 2px solid #DC2626 !important;
        }
        .cell-revealed {
            background-color: rgba(14, 165, 233, 0.1);
            color: #0284C7;
        }

        /* Notebook margins overlay */
        .red-line-left {
            position: absolute;
            left: 24px; /* Alignment next to coordinate letter column */
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: rgba(220, 38, 38, 0.5);
            z-index: 2;
            pointer-events: none;
        }
        .red-line-right {
            position: absolute;
            right: 24px;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: rgba(220, 38, 38, 0.5);
            z-index: 2;
            pointer-events: none;
        }

        /* Spiral binding */
        .spiral-binding {
            width: 45px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-around;
            height: 350px;
            opacity: 0.65;
            font-size: 19px;
            font-weight: bold;
            color: #2B3E90;
            border-left: 1px dashed rgba(43, 62, 144, 0.25);
            border-right: 1px dashed rgba(43, 62, 144, 0.25);
            margin: 0 15px;
        }

        /* Battle Inventory Displays */
        .battle-inventory {
            display: flex;
            gap: 8px;
            margin-top: 12px;
            width: 100%;
            justify-content: center;
        }
        .inv-item {
            border: 1.5px solid #2B3E90;
            border-radius: 4px;
            padding: 3px 8px;
            background-color: #F7F5EC;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 2px 2px 0px rgba(43, 62, 144, 0.1);
        }
        .inv-item.active {
            background-color: #FEF08A;
            box-shadow: none;
            transform: translateY(1px);
        }
        .inv-item.disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        /* Logs Panel */
        .battle-logs-wrapper {
            margin-top: 10px;
            width: 100%;
        }
        .battle-logs-header {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 3px;
        }
        .battle-logs-box {
            height: 95px;
            overflow-y: auto;
            border: 2px solid #2B3E90;
            border-radius: 6px;
            padding: 8px;
            background-color: #FDFDFB;
            font-size: 15px;
            color: #1E3A8A;
            box-shadow: inset 1px 1px 4px rgba(0,0,0,0.04);
        }
        .log-entry {
            border-bottom: 1px dashed rgba(43,62,144,0.08);
            padding-bottom: 2px;
            margin-bottom: 2px;
        }

        /* Bottom Online battles corner banner */
        .bottom-banner-wrapper {
            display: flex;
            justify-content: flex-end;
            margin-top: 5px;
            width: 100%;
        }
        .bottom-banner {
            background-color: #FAF8F2;
            border: 2px solid #2B3E90;
            border-radius: 4px;
            padding: 4px 18px;
            color: #2B3E90;
            font-weight: bold;
            font-size: 20px;
            transform: rotate(-1.5deg);
            box-shadow: 3px 3px 0px rgba(43,62,144,0.12);
        }

        /* Intermission Screen (Hotseat) */
        .intermission-overlay {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #FAF8F2;
            z-index: 100;
            text-align: center;
            padding: 30px;
        }
        .intermission-overlay.active {
            display: flex;
        }
        .inter-title {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .inter-desc {
            font-size: 20px;
            color: #5A6A85;
            margin-bottom: 25px;
        }

        /* Game Over Screen */
        .gameover-box {
            text-align: center;
            border: 3px solid #2B3E90;
            border-radius: 8px;
            padding: 25px;
            background-color: #FAF8F2;
            box-shadow: 6px 6px 0px rgba(43, 62, 144, 0.15);
            max-width: 460px;
            width: 100%;
            margin-top: 25px;
        }
        .go-title {
            font-size: 40px;
            font-weight: bold;
            margin-top: 0px;
            margin-bottom: 8px;
        }
        .go-title.win { color: #10B981; }
        .go-title.lose { color: #EF4444; }

        /* Animation Overlays */
        .anim-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 50;
            overflow: hidden;
            display: none;
        }
        .bomber-plane {
            position: absolute;
            width: 120px;
            transform: rotate(45deg);
            opacity: 0.85;
            top: -120px;
            left: -120px;
            transition: all 1.8s linear;
        }
        .bomber-shadow {
            position: absolute;
            width: 100px;
            transform: rotate(45deg);
            opacity: 0.15;
            top: -100px;
            left: -100px;
            transition: all 1.8s linear;
        }
        .torpedo-missile {
            position: absolute;
            width: 60px;
            top: 0;
            left: -80px;
            transition: all 0.8s ease-in;
        }

        /* Sound toggle button position */
        .audio-toggle-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            font-size: 24px;
            cursor: pointer;
            z-index: 10;
        }

        /* Coordinate numbers row styling */
        .board-numbers-row {
            display: flex;
            width: 345px;
            height: 25px;
        }
        .board-numbers-list {
            display: flex;
            flex: 1;
            justify-content: space-around;
            align-items: center;
            font-size: 16px;
            font-weight: bold;
            color: #2B3E90;
        }
        .board-numbers-list div {
            width: 32px;
            text-align: center;
        }

        /* Green hatched neighbors cells */
        .cell-neighbor {
            background: repeating-linear-gradient(45deg, rgba(16, 185, 129, 0.05), rgba(16, 185, 129, 0.05) 2px, rgba(16, 185, 129, 0.15) 2px, rgba(16, 185, 129, 0.15) 4px);
            border: 0.5px dashed rgba(16, 185, 129, 0.45) !important;
        }

        /* Hand-drawn button modifiers */
        .btn-green-handdrawn {
            border-color: #10B981 !important;
            color: #10B981 !important;
            box-shadow: 3px 5px 0px rgba(16, 185, 129, 0.15) !important;
        }
        .btn-green-handdrawn:hover {
            background-color: rgba(16, 185, 129, 0.08) !important;
        }

        /* Rotate button */
        .rotate-btn-handdrawn {
            position: absolute;
            top: 25px;
            left: 355px;
            width: 60px;
            height: 40px;
            border: 2.5px solid #2B3E90;
            border-radius: 8px 4px 6px 5px/5px 6px 4px 8px;
            background: #FAF8F2;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: bold;
            color: #2B3E90;
            cursor: pointer;
            box-shadow: 2px 3px 0px rgba(43, 62, 144, 0.12);
            transition: all 0.15s;
            z-index: 10;
            white-space: nowrap;
            gap: 2px;
        }
        .rotate-btn-handdrawn:hover {
            background-color: #FEF08A;
            transform: scale(1.05);
        }
        .rotate-btn-handdrawn:active {
            transform: scale(0.95);
        }

        /* Placement Screen Layout */
        .placement-instruction-text {
            font-size: 22px;
            font-weight: bold;
            color: #C2410C;
            text-align: center;
            margin-bottom: 15px;
            min-height: 28px;
        }
        .placement-layout {
            display: flex;
            gap: 40px;
            width: 100%;
            justify-content: center;
            align-items: flex-start;
            margin-bottom: 25px;
        }
        .placement-board-container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .placement-pool-container {
            display: flex;
            flex-direction: column;
            width: 340px;
            border: 2px dashed rgba(43, 62, 144, 0.3);
            border-radius: 8px 12px 10px 14px/12px 10px 14px 8px;
            padding: 15px;
            background-color: rgba(43, 62, 144, 0.01);
            min-height: 345px;
        }
        .pool-title {
            font-size: 19px;
            font-weight: bold;
            color: #2B3E90;
            margin-bottom: 15px;
            border-bottom: 2px dashed rgba(43, 62, 144, 0.25);
            padding-bottom: 5px;
            text-align: center;
        }
        .pool-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            min-height: 38px;
        }
        .pool-row-label {
            font-size: 15px;
            font-weight: bold;
            color: #5A6A85;
            width: 80px;
        }
        .pool-ships-list {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .pool-ship {
            display: flex;
            border: 2px solid #2B3E90;
            border-radius: 6px 3px 5px 4px/4px 5px 3px 6px;
            background-color: rgba(43, 62, 144, 0.05);
            padding: 2px;
            position: relative;
            transition: all 0.15s;
        }
        .pool-ship.active {
            background-color: #FEF08A;
            border-color: #C2410C;
            transform: scale(1.05);
            box-shadow: 0px 0px 6px rgba(194, 65, 12, 0.35);
        }
        .pool-ship.placed {
            opacity: 0.2;
        }
        .pool-ship-deck {
            width: 14px;
            height: 14px;
            border: 1px solid rgba(43, 62, 144, 0.45);
            background-color: transparent;
            margin: 1px;
        }
        .pool-ship.placed::after {
            content: "❌";
            position: absolute;
            font-size: 15px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #EF4444;
            font-weight: bold;
        }
        .placement-actions-row {
            display: flex;
            gap: 20px;
            width: 100%;
            max-width: 500px;
            justify-content: center;
            margin-top: 10px;
        }
        /* Drag-and-drop ghost ship styling */
        .drag-ghost {
            position: fixed;
            pointer-events: none;
            z-index: 1000;
            display: flex;
            opacity: 0.85;
            border: 2px dashed #2B3E90;
            background-color: #FEF08A; /* yellow highlight */
            border-radius: 6px;
            box-shadow: 4px 6px 12px rgba(43, 62, 144, 0.35);
        }
        .drag-ghost-deck {
            width: 32px;
            height: 32px;
            border: 1px solid rgba(43, 62, 144, 0.45);
        }

        /* Drag placement validation previews */
        .cell-drag-valid {
            background-color: rgba(16, 185, 129, 0.35) !important;
            border: 1.5px solid #10B981 !important;
        }
        .cell-drag-invalid {
            background-color: rgba(239, 68, 68, 0.35) !important;
            border: 1.5px solid #EF4444 !important;
        }
    </style>
</head>
<body>

    <!-- Margin doodles -->
    <svg class="doodle-anchor" viewBox="0 0 100 100" fill="none" stroke="#2B3E90" stroke-width="3">
        <path d="M50 15v60M30 65c0 10 10 15 20 15s20-5 20-15M25 65h10M65 65h10M50 15c-5 0-10-5-10-10s5-10 10-10 10 5 10 10-5 10-10 10z"/>
    </svg>
    <svg class="doodle-plane" viewBox="0 0 100 100" fill="none" stroke="#2B3E90" stroke-width="2.5">
        <path d="M10 50h80M50 15v70M35 30c5 5 15 5 20 0M30 70h40M45 40v20"/>
    </svg>
    <svg class="doodle-sub" viewBox="0 0 100 100" fill="none" stroke="#2B3E90" stroke-width="3">
        <rect x="25" y="45" width="50" height="20" rx="10"/>
        <path d="M50 45V30h10M40 30h5M65 65c-2 5-10 5-12 0M25 55H15M75 55h10"/>
    </svg>

    <div class="game-window">
        <!-- Audio switch -->
        <div class="audio-toggle-btn" id="audioToggleBtn" onclick="toggleAudio()">🔊</div>

        <!-- Top Header profiles bar -->
        <div class="top-profiles">
            <div class="red-margin-top"></div>
            <!-- Player 1 Profile -->
            <div class="profile-card" id="profileP1">
                <div class="avatar-box">🥷</div>
                <div class="profile-info">
                    <div class="profile-rank" id="rankP1">Моряк Новобранец</div>
                    <div class="profile-name" id="nameP1">captainboom</div>
                    <div class="profile-score" id="scoreP1">Счет: 0 XP</div>
                </div>
            </div>

            <!-- Turn indicator arrow -->
            <div class="turn-arrow" id="turnArrow">✏️</div>

            <!-- Player 2 / CPU Profile -->
            <div class="profile-card right" id="profileP2">
                <div class="avatar-box">🐙</div>
                <div class="profile-info">
                    <div class="profile-rank" id="rankP2">Моряк</div>
                    <div class="profile-name" id="nameP2">bestie</div>
                    <div class="profile-score" id="scoreP2">Счет: ИИ</div>
                </div>
            </div>
        </div>

        <!-- Animation overlay -->
        <div class="anim-overlay" id="animOverlay">
            <img class="bomber-plane" id="animPlane" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' fill='%232B3E90'><path d='M50 10 L60 40 L90 50 L60 60 L50 90 L40 60 L10 50 L40 40 Z'/></svg>">
            <img class="bomber-shadow" id="animPlaneShadow" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' fill='black'><path d='M50 10 L60 40 L90 50 L60 60 L50 90 L40 60 L10 50 L40 40 Z'/></svg>">
            <img class="torpedo-missile" id="animTorpedo" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' fill='%232B3E90'><rect x='20' y='40' width='60' height='20' rx='5'/><path d='M80 50 L70 40 L70 60 Z M20 40 L10 30 L10 70 Z'/></svg>">
        </div>

        <!-- Main game layout split -->
        <div class="main-layout">
            <!-- Sidebar Panel -->
            <div class="game-sidebar">
                <div class="sidebar-section-title">📓 НАСТРОЙКИ</div>
                
                <div class="sidebar-item" id="modeSelectWrapper">
                    <label style="font-weight:bold;">Режим игры:</label>
                    <select class="sidebar-select" id="gameModeSelect" onchange="onGameModeChange()">
                        <option value="Advanced">🚀 Расширенный</option>
                        <option value="Classic">⚓ Классический</option>
                    </select>
                </div>

                <div class="sidebar-item">
                    <label style="font-weight:bold;">Сложность ИИ:</label>
                    <select class="sidebar-select" id="difficultySelect">
                        <option value="Smart">🧠 Умный Бот</option>
                        <option value="Easy">🎲 Простой Бот</option>
                    </select>
                </div>

                <div class="sidebar-item" style="margin-top:5px;">
                    <label class="sidebar-checkbox-label">
                        <input type="checkbox" id="cheatModeSelect" onchange="renderBattleBoards()"> 🛰️ Разведка (Чит)
                    </label>
                </div>

                <div class="sidebar-section-title">🏆 ДОСТИЖЕНИЯ</div>
                <div class="sidebar-item" style="font-size:16px; font-weight:bold; line-height:1.4;">
                    <div>Ранг: <span style="color:#C2410C;" id="sidebarRank">Новобранец</span></div>
                    <div>Побед: <span id="sidebarWins">0</span></div>
                    <div>Поражений: <span id="sidebarLosses">0</span></div>
                    <div style="font-size:13px; color:#5A6A85; border-top:1px dashed #2B3E90; margin-top:5px; padding-top:3px;">
                        Победа: +1000 XP | Проигрыш: +150 XP
                    </div>
                </div>
            </div>

            <!-- Content Panel (Screens) -->
            <div class="game-content">

                <!-- Screen 1: Menu Screen -->
                <div class="screen active" id="screenMenu">
                    <div class="menu-title">МОРСКОЙ БОЙ 2</div>
                    <div class="menu-subtitle">ТАКТИЧЕСКИЙ ТЕТРАДНЫЙ СИМУЛЯТОР</div>
                    <div class="menu-buttons">
                        <button class="btn" onclick="startSetup(1)">🤖 Одиночная Игра (Против бота)</button>
                        <button class="btn" onclick="startSetup(2)">👥 Игра на Двоих (Hotseat)</button>
                    </div>
                </div>

                <!-- Screen 2: Shop / Arsenal Selection Screen -->
                <div class="screen" id="screenShop">
                    <div class="shop-title">🛒 ЗАКУПКА ТАКТИЧЕСКОГО ВООРУЖЕНИЯ</div>
                    <div class="shop-budget" id="shopBudget">Баланс: 1000 G</div>
                    <div class="shop-grid" id="shopGrid">
                        <!-- Shop items generated by JS -->
                    </div>
                    <button class="btn" style="max-width: 300px;" onclick="confirmArsenal()">Подтвердить Арсенал ➡️</button>
                </div>

                <!-- Screen 3: Placement Screen -->
                <div class="screen" id="screenPlacement">
                    <div class="placement-instruction-text" id="placementInstruction">Разместите 4-палубный корабль</div>
                    
                    <div class="placement-layout">
                        <!-- Left side: Board -->
                        <div class="placement-board-container">
                            <div class="board-wrapper">
                                <div class="board-title-text" id="placementBoardTitle">РАССТАНОВКА НАШИХ СУДОВ</div>
                                <div class="board-grid-outer">
                                    <div class="red-line-left"></div>
                                    
                                    <!-- Coordinate numbers row -->
                                    <div class="board-numbers-row">
                                        <div style="width: 25px;"></div>
                                        <div class="board-numbers-list" id="placementNumbers"></div>
                                    </div>
                                    
                                    <div style="display: flex;">
                                        <!-- Coordinate letters -->
                                        <div class="board-letters" id="placementLetters"></div>
                                        <!-- Grid -->
                                        <div class="board-grid" id="placementGrid"></div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Rotate button next to grid -->
                            <button class="rotate-btn-handdrawn" id="rotateBtn" onclick="togglePlacementOrientation()" title="Повернуть корабль">
                                🔄 ➡️
                            </button>
                        </div>
                        
                        <!-- Right side: Ships Pool -->
                        <div class="placement-pool-container">
                            <div class="pool-title">ДОСТУПНЫЕ КОРАБЛИ</div>
                            <div class="ships-pool" id="shipsPool"></div>
                            <div class="defenses-pool" id="defensesPool" style="display: none;"></div>
                        </div>
                    </div>
                    
                    <!-- Buttons under grid -->
                    <div class="placement-actions-row">
                        <button class="btn" style="width: auto; min-width: 120px;" onclick="autoPlaceAllCurrent()">🔄 Авто</button>
                        <button class="btn" style="width: auto; min-width: 140px;" onclick="clearPlacement()">🧹 Очистить</button>
                        <button class="btn btn-green-handdrawn" id="btnPlacementFight" style="display: none; width: auto; min-width: 140px;" onclick="finishPlacement()">⚔️ В БОЙ!</button>
                    </div>
                </div>

                <!-- Screen 4: Battle Screen -->
                <div class="screen" id="screenBattle">
                    <div class="battle-container">
                        <!-- Player 1 Board -->
                        <div class="board-wrapper">
                            <div class="board-title-text left" id="titleBoardLeft">🛡️ НАШ ФЛОТ</div>
                            <div class="board-grid-outer">
                                <div class="red-line-left"></div>
                                
                                <div class="board-numbers-row">
                                    <div style="width: 25px;"></div>
                                    <div class="board-numbers-list" id="battleNumbersLeft"></div>
                                </div>
                                
                                <div style="display: flex;">
                                    <div class="board-letters" id="battleLettersLeft"></div>
                                    <div class="board-grid" id="boardGridLeft"></div>
                                </div>
                            </div>
                            <div class="battle-inventory" id="battleInvLeft"></div>
                        </div>

                        <!-- Notebook Spirals -->
                        <div class="spiral-binding">
                            ➰<br>➰<br>➰<br>➰<br>➰<br>➰<br>➰<br>➰<br>➰<br>➰<br>➰<br>➰
                        </div>

                        <!-- Player 2 / CPU Board -->
                        <div class="board-wrapper">
                            <div class="board-title-text right" id="titleBoardRight">🛰️ РАДАР ПРОТИВНИКА</div>
                            <div class="board-grid-outer">
                                <div class="red-line-right"></div>
                                
                                <div class="board-numbers-row">
                                    <div class="board-numbers-list" id="battleNumbersRight"></div>
                                    <div style="width: 25px;"></div>
                                </div>
                                
                                <div style="display: flex;">
                                    <div class="board-grid" id="boardGridRight"></div>
                                    <div class="board-letters" id="battleLettersRight"></div>
                                </div>
                            </div>
                            <div class="battle-inventory" id="battleInvRight"></div>
                        </div>
                    </div>

                    <!-- Battle logs (Hidden) -->
                    <div class="battle-logs-wrapper" style="display: none !important;">
                        <div class="battle-logs-header">📜 БОРТОВОЙ ЖУРНАЛ СРАЖЕНИЯ:</div>
                        <div class="battle-logs-box" id="battleLogsBox"></div>
                    </div>
                    
                    <!-- Bottom notebook corner banner -->
                    <div class="bottom-banner-wrapper">
                        <div class="bottom-banner">ОНЛАЙН БОИ</div>
                    </div>
                </div>

                <!-- Screen 5: Intermission Screen -->
                <div class="intermission-overlay" id="intermissionOverlay">
                    <div class="inter-title" id="interTitle">ХОД ПЕРЕДАН!</div>
                    <div class="inter-desc" id="interDesc">Передайте устройство следующему игроку.</div>
                    <button class="btn" style="max-width:300px;" onclick="endIntermission()">Я ГОТОВ, НАЧАТЬ ХОД! 👁️</button>
                </div>

                <!-- Screen 6: Game Over Screen -->
                <div class="screen" id="screenGameOver">
                    <div class="gameover-box">
                        <div class="go-title win" id="goTitle">ПОБЕДА!</div>
                        <div style="font-size:22px; margin-bottom:15px;" id="goDesc">Все корабли вражеской эскадры потоплены.</div>
                        <div style="font-size:18px; color:#5A6A85; margin-bottom:20px;" id="goStats">Снарядов выпущено: 34</div>
                        <button class="btn" style="max-width:260px;" onclick="goToMenu()">В Главное Меню</button>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- AUDIO ENGINE AND GAME STATE LOGIC -->
    <script>
        // --- SOUND EFFECTS SYNTHESIZER (Web Audio API) ---
        let audioMuted = false;
        let audioCtx = null;

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
        }

        function toggleAudio() {
            audioMuted = !audioMuted;
            document.getElementById("audioToggleBtn").innerText = audioMuted ? "🔇" : "🔊";
        }

        // Procedural sounds
        function playSketchSound() {
            if (audioMuted) return;
            initAudio();
            const bufferSize = audioCtx.sampleRate * 0.08;
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            const noise = audioCtx.createBufferSource();
            noise.buffer = buffer;
            const filter = audioCtx.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = 1000;
            const gain = audioCtx.createGain();
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.07);
            
            noise.connect(filter);
            filter.connect(gain);
            gain.connect(audioCtx.destination);
            noise.start();
        }

        function playShotSound() {
            if (audioMuted) return;
            initAudio();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(600, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(120, audioCtx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.3);
        }

        function playMissSound() {
            if (audioMuted) return;
            initAudio();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(150, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.4);
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.4);
        }

        function playExplosionSound() {
            if (audioMuted) return;
            initAudio();
            const bufferSize = audioCtx.sampleRate * 0.45;
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            const noise = audioCtx.createBufferSource();
            noise.buffer = buffer;
            const filter = audioCtx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(350, audioCtx.currentTime);
            filter.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.45);
            const gain = audioCtx.createGain();
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.45);
            
            noise.connect(filter);
            filter.connect(gain);
            gain.connect(audioCtx.destination);
            noise.start();
        }

        function playSunkSound() {
            if (audioMuted) return;
            playExplosionSound();
            setTimeout(() => {
                initAudio();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(110, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.6);
                gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.6);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.6);
            }, 100);
        }

        function playPvoSound() {
            if (audioMuted) return;
            initAudio();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(200, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1800, audioCtx.currentTime + 0.4);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.4);
        }

        function playVictorySound() {
            if (audioMuted) return;
            initAudio();
            const notes = [261.63, 329.63, 392.00, 523.25, 392.00, 523.25];
            const durs = [0.15, 0.15, 0.15, 0.15, 0.15, 0.4];
            let time = audioCtx.currentTime;
            notes.forEach((freq, idx) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, time);
                gain.gain.setValueAtTime(0.15, time);
                gain.gain.exponentialRampToValueAtTime(0.01, time + durs[idx]);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(time);
                osc.stop(time + durs[idx]);
                time += durs[idx] - 0.02;
            });
        }

        function playDefeatSound() {
            if (audioMuted) return;
            initAudio();
            const notes = [392.00, 349.23, 311.13, 261.63];
            const durs = [0.2, 0.2, 0.2, 0.5];
            let time = audioCtx.currentTime;
            notes.forEach((freq, idx) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, time);
                gain.gain.setValueAtTime(0.15, time);
                gain.gain.exponentialRampToValueAtTime(0.01, time + durs[idx]);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(time);
                osc.stop(time + durs[idx]);
                time += durs[idx] - 0.02;
            });
        }

        // Custom HTML floating Toast Notification System
        function showToast(message, icon = "📢") {
            const toast = document.createElement("div");
            toast.style.position = "absolute";
            toast.style.bottom = "20px";
            toast.style.right = "20px";
            toast.style.background = "#FAF8F2";
            toast.style.border = "2px solid #2B3E90";
            toast.style.borderRadius = "4px";
            toast.style.padding = "10px 20px";
            toast.style.boxShadow = "4px 4px 0px rgba(43, 62, 144, 0.15)";
            toast.style.zIndex = "1000";
            toast.style.fontWeight = "bold";
            toast.style.display = "flex";
            toast.style.alignItems = "center";
            toast.style.gap = "10px";
            toast.style.fontSize = "18px";
            toast.style.color = "#2B3E90";
            toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
            
            document.querySelector(".game-window").appendChild(toast);
            
            // Slide out
            setTimeout(() => {
                toast.style.transition = "all 0.5s ease";
                toast.style.opacity = "0";
                toast.style.transform = "translateY(20px)";
                setTimeout(() => { toast.remove(); }, 500);
            }, 2000);
        }


        // --- CORE GAME STATE ---
        const LETTERS = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"];
        
        let gameMode = 'Advanced'; // Classic, Advanced
        let playerCount = 1;       // 1, 2
        let currentTurn = 'P1';     // P1, P2 / CPU
        let gamePhase = 'MENU';    // MENU, SHOP, PLACING, PLAYING, GAMEOVER
        let selectedDefenseType = 'mine';
        
        // Ship Placement State
        let poolShipsPlaced = [false, false, false, false, false, false, false, false, false, false];
        const SHIP_SIZES_BY_INDEX = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1];
        
        // Drag-and-drop state variables
        let isDragging = false;
        let dragIdx = -1;
        let dragSize = -1;
        let dragGhost = null;
        let lastX = 0;
        let lastY = 0;
        
        // Profiles
        let stats = {
            P1: { xp: 0, rank: 'Новобранец', wins: 0, losses: 0 },
            P2: { xp: 0, rank: 'Новобранец', wins: 0, losses: 0 }
        };

        // Weapon Shop specs
        const WEAPON_SPECS = {
            mine: { name: "Мина", cost: 200, max: 2, icon: "💣", desc: "Урон врагу + бесплатный выстрел" },
            pvo: { name: "ПВО", cost: 300, max: 1, icon: "🛡️", desc: "Сбивает вражеские авиаудары" },
            radar: { name: "Радар", cost: 200, max: 3, icon: "🛰️", desc: "Сканирует 3х3. Без урона." },
            torpedo: { name: "Торпеда", cost: 300, max: 2, icon: "🚀", desc: "Поражает первый корабль в ряду" },
            bomber: { name: "Авиаудар", cost: 400, max: 2, icon: "🛩️", desc: "Бомбит зону 3х3" }
        };

        // Inventories
        let p1Inventory = { mine: 0, pvo: 0, radar: 0, torpedo: 0, bomber: 0 };
        let p2Inventory = { mine: 0, pvo: 0, radar: 0, torpedo: 0, bomber: 0 };

        let p1Board = Array(10).fill().map(() => Array(10).fill(0));
        let p2Board = Array(10).fill().map(() => Array(10).fill(0));
        let p1Ships = [];
        let p2Ships = [];

        // Active weapon targeting selection
        let activeWeapon = null;

        // Bot Hunter states
        let cpuHunter = {
            state: 'hunt', // hunt, target
            hits: [],
            inventory: { mine: 0, pvo: 0, radar: 0, torpedo: 0, bomber: 0 }
        };

        // Statistics counters
        let matchStats = {
            p1Shots: 0,
            p2Shots: 0,
            p1Hits: 0,
            p2Hits: 0
        };

        // Loading profile persistence
        function loadProfile() {
            const stored = localStorage.getItem('seabattle2_profile_v2');
            if (stored) {
                try {
                    const parsed = JSON.parse(stored);
                    stats.P1.xp = parsed.xp || 0;
                    stats.P1.wins = parsed.wins || 0;
                    stats.P1.losses = parsed.losses || 0;
                    updateRank('P1');
                } catch(e) {}
            }
            updateRankHeader();
        }

        function saveProfile() {
            const profileData = {
                xp: stats.P1.xp,
                wins: stats.P1.wins,
                losses: stats.P1.losses
            };
            localStorage.setItem('seabattle2_profile_v2', JSON.stringify(profileData));
        }

        function updateRank(player) {
            const xp = stats[player].xp;
            let rank = 'Новобранец';
            if (xp >= 1000 && xp < 2500) rank = 'Матрос';
            else if (xp >= 2500 && xp < 5000) rank = 'Старшина';
            else if (xp >= 5000 && xp < 10000) rank = 'Мичман';
            else if (xp >= 10000 && xp < 20000) rank = 'Капитан';
            else if (xp >= 20000) rank = 'Адмирал';
            stats[player].rank = rank;
        }

        function updateRankHeader() {
            document.getElementById("rankP1").innerText = stats.P1.rank;
            document.getElementById("scoreP1").innerText = "Счет: " + stats.P1.xp + " XP";
            
            document.getElementById("nameP2").innerText = playerCount === 2 ? "Игрок 2" : "bestie";
            document.getElementById("rankP2").innerText = playerCount === 2 ? stats.P2.rank : "Моряк";
            document.getElementById("scoreP2").innerText = playerCount === 2 ? "Счет: " + stats.P2.xp + " XP" : "Счет: ИИ";

            // Sidebar stats
            document.getElementById("sidebarRank").innerText = stats.P1.rank;
            document.getElementById("sidebarWins").innerText = stats.P1.wins;
            document.getElementById("sidebarLosses").innerText = stats.P1.losses;
        }

        // --- SCREEN NAVIGATION ---
        function showScreen(screenId) {
            document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
            document.getElementById(screenId).classList.add("active");
        }

        function goToMenu() {
            gamePhase = 'MENU';
            document.getElementById("turnArrow").innerText = "✏️";
            document.getElementById("profileP1").classList.remove("active");
            document.getElementById("profileP2").classList.remove("active");
            document.getElementById("modeSelectWrapper").style.display = "block"; // allow setting mode
            updateRankHeader();
            showScreen("screenMenu");
        }

        function onGameModeChange() {
            gameMode = document.getElementById("gameModeSelect").value;
        }

        // --- MENU SCREEN CONTROLLER ---
        function startSetup(players) {
            playSketchSound();
            playerCount = players;
            gameMode = document.getElementById("gameModeSelect").value;
            document.getElementById("modeSelectWrapper").style.display = "none"; // lock mode during match
            
            loadProfile();
            
            // Clean board structures
            p1Board = Array(10).fill().map(() => Array(10).fill(0));
            p2Board = Array(10).fill().map(() => Array(10).fill(0));
            p1Ships = [];
            p2Ships = [];
            matchStats = { p1Shots: 0, p2Shots: 0, p1Hits: 0, p2Hits: 0 };
            
            p1Inventory = { mine: 0, pvo: 0, radar: 0, torpedo: 0, bomber: 0 };
            p2Inventory = { mine: 0, pvo: 0, radar: 0, torpedo: 0, bomber: 0 };
            
            updateRankHeader();

            if (gameMode === 'Advanced') {
                setupShopPhase('P1');
            } else {
                setupPlacementPhase('P1');
            }
        }

        // --- ARSENAL SHOP CONTROLLER ---
        let currentShopPlayer = 'P1';
        let shopTempInventory = {};
        let shopTempBudget = 1000;

        function setupShopPhase(player) {
            currentShopPlayer = player;
            shopTempInventory = { mine: 0, pvo: 0, radar: 0, torpedo: 0, bomber: 0 };
            shopTempBudget = 1000;
            
            document.getElementById("turnArrow").innerText = player === 'P1' ? "◀" : "▶";
            document.getElementById("shopBudget").innerText = "Баланс: " + shopTempBudget + " G";
            
            renderShop();
            showScreen("screenShop");
        }

        function renderShop() {
            const grid = document.getElementById("shopGrid");
            grid.innerHTML = "";
            
            Object.keys(WEAPON_SPECS).forEach(key => {
                const item = WEAPON_SPECS[key];
                const card = document.createElement("div");
                card.className = "shop-card";
                
                const qty = shopTempInventory[key] || 0;
                
                card.innerHTML = `
                    <div class="shop-card-icon">${item.icon}</div>
                    <div class="shop-card-name">${item.name}</div>
                    <div class="shop-card-cost">${item.cost} G</div>
                    <div style="font-size:11px; color:#5A6A85; min-height:28px; margin-bottom:8px; line-height:1.2;">${item.desc}</div>
                    <div class="shop-card-controls">
                        <div class="shop-btn-circle" onclick="changeShopQty('${key}', -1)">-</div>
                        <div class="shop-card-qty">${qty}</div>
                        <div class="shop-btn-circle" onclick="changeShopQty('${key}', 1)">+</div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function changeShopQty(key, delta) {
            const spec = WEAPON_SPECS[key];
            const currentQty = shopTempInventory[key] || 0;
            
            if (delta > 0) {
                // Check max constraint
                if (currentQty >= spec.max) {
                    showToast("Достигнут предел покупки этого оружия!", "⚠️");
                    return;
                }
                // Check budget
                if (shopTempBudget < spec.cost) {
                    showToast("Недостаточно золота для покупки!", "🪙");
                    return;
                }
                shopTempInventory[key]++;
                shopTempBudget -= spec.cost;
                playSketchSound();
            } else {
                if (currentQty <= 0) return;
                shopTempInventory[key]--;
                shopTempBudget += spec.cost;
                playSketchSound();
            }
            
            document.getElementById("shopBudget").innerText = "Баланс: " + shopTempBudget + " G";
            renderShop();
        }

        function confirmArsenal() {
            playSketchSound();
            // Store inventory
            const targetInv = currentShopPlayer === 'P1' ? p1Inventory : p2Inventory;
            Object.keys(shopTempInventory).forEach(k => {
                targetInv[k] = shopTempInventory[k];
            });

            if (playerCount === 2 && currentShopPlayer === 'P1') {
                // Player 2 shop phase
                setupShopPhase('P2');
            } else {
                // Proceed to placements
                if (playerCount === 1) {
                    // Generate CPU random arsenal
                    generateCpuArsenal();
                }
                setupPlacementPhase('P1');
            }
        }

        function generateCpuArsenal() {
            cpuHunter.inventory = { mine: 0, pvo: 0, radar: 0, torpedo: 0, bomber: 0 };
            let cpuBudget = 1000;
            const keys = Object.keys(WEAPON_SPECS);
            let attempts = 0;
            
            while (cpuBudget >= 200 && attempts < 100) {
                attempts++;
                const key = keys[Math.floor(Math.random() * keys.length)];
                const spec = WEAPON_SPECS[key];
                if (cpuBudget >= spec.cost && cpuHunter.inventory[key] < spec.max) {
                    cpuHunter.inventory[key]++;
                    cpuBudget -= spec.cost;
                }
            }
        }


        // --- SHIP PLACEMENT CONTROLLER ---
        let currentPlacementPlayer = 'P1';
        let placementShipsLeft = [];
        let placementOrientation = 'H';
        let placedDefenseCount = { mine: 0, pvo: 0 };

        function setupPlacementPhase(player) {
            currentPlacementPlayer = player;
            poolShipsPlaced = Array(10).fill(false);
            placementOrientation = 'H';
            
            const pInv = player === 'P1' ? p1Inventory : p2Inventory;
            placedDefenseCount = { mine: pInv.mine, pvo: pInv.pvo };
            selectedDefenseType = placedDefenseCount.mine > 0 ? 'mine' : 'pvo';

            document.getElementById("turnArrow").innerText = player === 'P1' ? "◀" : "▶";
            document.getElementById("placementBoardTitle").innerText = player === 'P1' ? "РАССТАНОВКА НАШИХ СУДОВ" : "РАССТАНОВКА ФЛОТА ИГРОКА 2";
            
            // Highlight active profile card during placement
            if (player === 'P1') {
                document.getElementById("profileP1").classList.add("active");
                document.getElementById("profileP2").classList.remove("active");
            } else {
                document.getElementById("profileP1").classList.remove("active");
                document.getElementById("profileP2").classList.add("active");
            }

            renderPlacementGrid();
            renderPlacementLetters();
            renderPlacementNumbers();
            updatePlacementOrientationUI();
            updatePlacementUI();
            
            showScreen("screenPlacement");
        }

        function renderPlacementLetters() {
            const container = document.getElementById("placementLetters");
            container.innerHTML = "";
            LETTERS.forEach(l => {
                const d = document.createElement("div");
                d.className = "grid-row-header";
                d.innerText = l;
                container.appendChild(d);
            });
        }

        function renderPlacementNumbers() {
            const container = document.getElementById("placementNumbers");
            if (!container) return;
            container.innerHTML = "";
            for (let i = 1; i <= 10; i++) {
                const d = document.createElement("div");
                d.innerText = i;
                container.appendChild(d);
            }
        }

        function getPlacementNeighbors(board, shipsList) {
            const neighbors = Array(10).fill().map(() => Array(10).fill(false));
            shipsList.forEach(ship => {
                ship.coords.forEach(([r, c]) => {
                    for (let dr = -1; dr <= 1; dr++) {
                        for (let dc = -1; dc <= 1; dc++) {
                            const nr = r + dr;
                            const nc = c + dc;
                            if (nr >= 0 && nr < 10 && nc >= 0 && nc < 10) {
                                neighbors[nr][nc] = true;
                            }
                        }
                    }
                });
            });
            shipsList.forEach(ship => {
                ship.coords.forEach(([r, c]) => {
                    neighbors[r][c] = false;
                });
            });
            return neighbors;
        }

        function renderPlacementGrid() {
            const grid = document.getElementById("placementGrid");
            grid.innerHTML = "";
            const board = currentPlacementPlayer === 'P1' ? p1Board : p2Board;
            const shipsList = currentPlacementPlayer === 'P1' ? p1Ships : p2Ships;
            const neighbors = getPlacementNeighbors(board, shipsList);
            
            for (let r = 0; r < 10; r++) {
                for (let c = 0; c < 10; c++) {
                    const cell = document.createElement("div");
                    cell.className = "cell";
                    
                    const val = board[r][c];
                    if (val === 1) {
                        cell.innerText = "⛵";
                        cell.style.color = "#2B3E90";
                    } else if (val === 6) {
                        cell.innerText = "💣";
                    } else if (val === 7) {
                        cell.innerText = "🛡️";
                    } else if (neighbors[r][c]) {
                        cell.classList.add("cell-neighbor");
                    }
                    
                    cell.onclick = () => onPlacementCellClick(r, c);
                    grid.appendChild(cell);
                }
            }
        }

        function renderShipsPool() {
            const container = document.getElementById("shipsPool");
            if (!container) return;
            container.innerHTML = "";
            
            const sizes = [4, 3, 2, 1];
            const rowIndices = {
                4: [0],
                3: [1, 2],
                2: [3, 4, 5],
                1: [6, 7, 8, 9]
            };
            
            sizes.forEach(size => {
                const row = document.createElement("div");
                row.className = "pool-row";
                
                const label = document.createElement("div");
                label.className = "pool-row-label";
                label.innerText = `${size}-палубный`;
                row.appendChild(label);
                
                const list = document.createElement("div");
                list.className = "pool-ships-list";
                
                const indices = rowIndices[size];
                indices.forEach(idx => {
                    const poolShip = document.createElement("div");
                    poolShip.className = "pool-ship";
                    
                    for (let d = 0; d < size; d++) {
                        const deck = document.createElement("div");
                        deck.className = "pool-ship-deck";
                        poolShip.appendChild(deck);
                    }
                    
                    const isPlaced = poolShipsPlaced[idx];
                    if (isPlaced) {
                        poolShip.classList.add("placed");
                    } else {
                        poolShip.style.cursor = "grab";
                        poolShip.onmousedown = (e) => onShipDragStart(e, idx, size);
                        poolShip.ontouchstart = (e) => onShipDragStart(e, idx, size);
                    }
                    
                    const firstUnplacedIdx = poolShipsPlaced.indexOf(false);
                    if (idx === firstUnplacedIdx && !isPlaced) {
                        poolShip.classList.add("active");
                    }
                    
                    list.appendChild(poolShip);
                });
                
                row.appendChild(list);
                container.appendChild(row);
            });
        }

        function selectDefenseType(type) {
            playSketchSound();
            selectedDefenseType = type;
            updatePlacementUI();
        }

        function updatePlacementUI() {
            const numPlaced = poolShipsPlaced.filter(p => p).length;
            const instr = document.getElementById("placementInstruction");
            const btnFight = document.getElementById("btnPlacementFight");
            
            if (numPlaced < 10) {
                const firstUnplacedIdx = poolShipsPlaced.indexOf(false);
                const nextSize = firstUnplacedIdx !== -1 ? SHIP_SIZES_BY_INDEX[firstUnplacedIdx] : 0;
                instr.innerHTML = `👉 Перетащите <b>${nextSize}-палубный</b> корабль на поле (${numPlaced + 1} из 10)`;
                btnFight.style.display = "none";
            } else if (gameMode === 'Advanced' && (placedDefenseCount.mine > 0 || placedDefenseCount.pvo > 0)) {
                if (placedDefenseCount.mine > 0 && selectedDefenseType === 'mine') {
                    instr.innerHTML = `💣 Установите <b>мину</b> на воду (${placedDefenseCount.mine} шт. осталось)`;
                } else if (placedDefenseCount.pvo > 0 && selectedDefenseType === 'pvo') {
                    instr.innerHTML = `🛡️ Установите <b>ПВО</b> на воду (${placedDefenseCount.pvo} шт. осталось)`;
                } else {
                    instr.innerHTML = `🛡️ Выберите средство обороны для установки`;
                }
                btnFight.style.display = "none";
            } else {
                instr.innerHTML = `🎉 Все готово к бою! Вперед!`;
                btnFight.style.display = "inline-flex";
            }
            
            // Update defenses pool
            const defContainer = document.getElementById("defensesPool");
            if (gameMode === 'Advanced' && numPlaced === 10) {
                defContainer.style.display = "block";
                defContainer.innerHTML = `
                    <div class="pool-title" style="margin-top: 15px;">СРЕДСТВА ОБОРОНЫ</div>
                    <div style="display:flex; flex-direction:column; gap:10px;">
                        <div class="pool-row ${selectedDefenseType === 'mine' ? 'active' : ''}" style="cursor: pointer; padding: 5px; border-radius: 4px;" onclick="selectDefenseType('mine')">
                            <div class="pool-row-label">💣 Мина</div>
                            <div style="font-size:17px; font-weight:bold; color:#2B3E90;">
                                ${placedDefenseCount.mine > 0 ? "x" + placedDefenseCount.mine + " (Выбрать)" : "✅ Установлено"}
                            </div>
                        </div>
                        <div class="pool-row ${selectedDefenseType === 'pvo' ? 'active' : ''}" style="cursor: pointer; padding: 5px; border-radius: 4px;" onclick="selectDefenseType('pvo')">
                            <div class="pool-row-label">🛡️ ПВО</div>
                            <div style="font-size:17px; font-weight:bold; color:#2B3E90;">
                                ${placedDefenseCount.pvo > 0 ? "x" + placedDefenseCount.pvo + " (Выбрать)" : "✅ Установлено"}
                            </div>
                        </div>
                    </div>
                `;
            } else {
                defContainer.style.display = "none";
            }

            renderPlacementGrid();
            renderShipsPool();
        }

        function togglePlacementOrientation() {
            playSketchSound();
            placementOrientation = placementOrientation === 'H' ? 'V' : 'H';
            updatePlacementOrientationUI();
        }

        function updatePlacementOrientationUI() {
            const rotateBtn = document.getElementById("rotateBtn");
            if (rotateBtn) {
                rotateBtn.innerHTML = placementOrientation === 'H' ? '🔄 ➡️' : '🔄 ⬇️';
            }
        }

        // --- DRAG AND DROP ENGINE ---
        function onShipDragStart(e, idx, size) {
            if (poolShipsPlaced[idx]) return;
            
            isDragging = true;
            dragIdx = idx;
            dragSize = size;
            
            if (dragGhost) {
                dragGhost.remove();
            }
            
            dragGhost = document.createElement("div");
            dragGhost.className = "drag-ghost";
            dragGhost.style.flexDirection = placementOrientation === 'H' ? 'row' : 'column';
            
            for (let i = 0; i < size; i++) {
                const deck = document.createElement("div");
                deck.className = "drag-ghost-deck";
                dragGhost.appendChild(deck);
            }
            document.body.appendChild(dragGhost);
            
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            lastX = clientX;
            lastY = clientY;
            updateGhostPosition(clientX, clientY);
            
            document.addEventListener('mousemove', onShipDragMove);
            document.addEventListener('touchmove', onShipDragMove, { passive: false });
            document.addEventListener('mouseup', onShipDragEnd);
            document.addEventListener('touchend', onShipDragEnd);
        }

        function updateGhostPosition(clientX, clientY) {
            if (!dragGhost) return;
            dragGhost.style.left = (clientX - 16) + "px";
            dragGhost.style.top = (clientY - 16) + "px";
        }

        function updateGhostOrientation() {
            if (dragGhost) {
                dragGhost.style.flexDirection = placementOrientation === 'H' ? 'row' : 'column';
            }
        }

        function onShipDragMove(e) {
            if (!isDragging) return;
            
            if (e.cancelable) {
                e.preventDefault();
            }
            
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            lastX = clientX;
            lastY = clientY;
            
            updateGhostPosition(clientX, clientY);
            
            const grid = document.getElementById("placementGrid");
            if (!grid) return;
            
            const rect = grid.getBoundingClientRect();
            if (clientX >= rect.left && clientX <= rect.right && clientY >= rect.top && clientY <= rect.bottom) {
                const x = clientX - rect.left;
                const y = clientY - rect.top;
                const c = Math.floor(x / 32);
                const r = Math.floor(y / 32);
                
                let coords = [];
                if (placementOrientation === 'H') {
                    for (let i = 0; i < dragSize; i++) coords.push([r, c + i]);
                } else {
                    for (let i = 0; i < dragSize; i++) coords.push([r + i, c]);
                }
                
                const board = currentPlacementPlayer === 'P1' ? p1Board : p2Board;
                const isValid = jsCheckPlacementValid(board, coords);
                
                highlightPlacementPreview(coords, isValid);
            } else {
                clearPlacementPreview();
            }
        }

        function onShipDragEnd(e) {
            if (!isDragging) return;
            
            document.removeEventListener('mousemove', onShipDragMove);
            document.removeEventListener('touchmove', onShipDragMove);
            document.removeEventListener('mouseup', onShipDragEnd);
            document.removeEventListener('touchend', onShipDragEnd);
            
            const grid = document.getElementById("placementGrid");
            if (grid) {
                const rect = grid.getBoundingClientRect();
                if (lastX >= rect.left && lastX <= rect.right && lastY >= rect.top && lastY <= rect.bottom) {
                    const x = lastX - rect.left;
                    const y = lastY - rect.top;
                    const c = Math.floor(x / 32);
                    const r = Math.floor(y / 32);
                    
                    const board = currentPlacementPlayer === 'P1' ? p1Board : p2Board;
                    const shipsList = currentPlacementPlayer === 'P1' ? p1Ships : p2Ships;
                    
                    let coords = [];
                    if (placementOrientation === 'H') {
                        for (let i = 0; i < dragSize; i++) coords.push([r, c + i]);
                    } else {
                        for (let i = 0; i < dragSize; i++) coords.push([r + i, c]);
                    }
                    
                    if (jsCheckPlacementValid(board, coords)) {
                        coords.forEach(([rc, cc]) => {
                            board[rc][cc] = 1;
                        });
                        shipsList.push({
                            size: dragSize,
                            coords: coords,
                            sunk: false
                        });
                        poolShipsPlaced[dragIdx] = true;
                        playSketchSound();
                    } else {
                        playPvoSound();
                        showToast("Невозможно разместить корабль сюда!", "❌");
                    }
                }
            }
            
            clearPlacementPreview();
            
            if (dragGhost) {
                dragGhost.remove();
                dragGhost = null;
            }
            
            isDragging = false;
            dragIdx = -1;
            dragSize = -1;
            
            updatePlacementUI();
        }

        function highlightPlacementPreview(coords, isValid) {
            clearPlacementPreview();
            const grid = document.getElementById("placementGrid");
            if (!grid) return;
            
            const cells = grid.children;
            coords.forEach(([r, c]) => {
                if (r >= 0 && r < 10 && c >= 0 && c < 10) {
                    const cellIdx = r * 10 + c;
                    const cell = cells[cellIdx];
                    if (cell) {
                        cell.classList.add(isValid ? "cell-drag-valid" : "cell-drag-invalid");
                    }
                }
            });
        }

        function clearPlacementPreview() {
            const grid = document.getElementById("placementGrid");
            if (!grid) return;
            const cells = grid.children;
            for (let i = 0; i < cells.length; i++) {
                cells[i].classList.remove("cell-drag-valid", "cell-drag-invalid");
            }
        }

        function onPlacementCellClick(r, c) {
            const board = currentPlacementPlayer === 'P1' ? p1Board : p2Board;
            const shipsList = currentPlacementPlayer === 'P1' ? p1Ships : p2Ships;
            
            const firstUnplacedIdx = poolShipsPlaced.indexOf(false);
            if (firstUnplacedIdx !== -1) {
                const size = SHIP_SIZES_BY_INDEX[firstUnplacedIdx];
                let coords = [];
                if (placementOrientation === 'H') {
                    for (let i = 0; i < size; i++) coords.push([r, c + i]);
                } else {
                    for (let i = 0; i < size; i++) coords.push([r + i, c]);
                }
                
                if (jsCheckPlacementValid(board, coords)) {
                    coords.forEach(([rc, cc]) => {
                        board[rc][cc] = 1;
                    });
                    shipsList.push({
                        size: size,
                        coords: coords,
                        sunk: false
                    });
                    poolShipsPlaced[firstUnplacedIdx] = true;
                    playSketchSound();
                    updatePlacementUI();
                } else {
                    playPvoSound();
                    showToast("Невозможно разместить корабль сюда!", "❌");
                }
            } else if (gameMode === 'Advanced') {
                if (board[r][c] === 6) {
                    board[r][c] = 0;
                    placedDefenseCount.mine++;
                    playSketchSound();
                    updatePlacementUI();
                } else if (board[r][c] === 7) {
                    board[r][c] = 0;
                    placedDefenseCount.pvo++;
                    playSketchSound();
                    updatePlacementUI();
                } else if (board[r][c] === 0) {
                    const defType = selectedDefenseType;
                    if (defType === 'mine' && placedDefenseCount.mine > 0) {
                        board[r][c] = 6;
                        placedDefenseCount.mine--;
                        playSketchSound();
                    } else if (defType === 'pvo' && placedDefenseCount.pvo > 0) {
                        board[r][c] = 7;
                        placedDefenseCount.pvo--;
                        playSketchSound();
                    }
                    if (selectedDefenseType === 'mine' && placedDefenseCount.mine === 0 && placedDefenseCount.pvo > 0) {
                        selectedDefenseType = 'pvo';
                    } else if (selectedDefenseType === 'pvo' && placedDefenseCount.pvo === 0 && placedDefenseCount.mine > 0) {
                        selectedDefenseType = 'mine';
                    }
                    updatePlacementUI();
                } else {
                    showToast("Оборону можно размещать только в воду!", "🌊");
                }
            }
        }

        function jsCheckPlacementValid(board, coords) {
            for (let i = 0; i < coords.length; i++) {
                const [r, c] = coords[i];
                if (r < 0 || r >= 10 || c < 0 || c >= 10) return false;
                if (board[r][c] !== 0) return false;
                
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        const nr = r + dr;
                        const nc = c + dc;
                        if (nr >= 0 && nr < 10 && nc >= 0 && nc < 10) {
                            if (board[nr][nc] === 1) return false;
                        }
                    }
                }
            }
            return true;
        }

        function clearPlacement() {
            playSketchSound();
            const board = currentPlacementPlayer === 'P1' ? p1Board : p2Board;
            const shipsList = currentPlacementPlayer === 'P1' ? p1Ships : p2Ships;
            
            for (let r = 0; r < 10; r++) {
                for (let c = 0; c < 10; c++) board[r][c] = 0;
            }
            shipsList.length = 0;
            poolShipsPlaced = Array(10).fill(false);
            
            const pInv = currentPlacementPlayer === 'P1' ? p1Inventory : p2Inventory;
            placedDefenseCount = { mine: pInv.mine, pvo: pInv.pvo };
            selectedDefenseType = placedDefenseCount.mine > 0 ? 'mine' : 'pvo';
            
            updatePlacementUI();
        }

        function autoPlaceAllCurrent() {
            playSketchSound();
            const board = currentPlacementPlayer === 'P1' ? p1Board : p2Board;
            const shipsList = currentPlacementPlayer === 'P1' ? p1Ships : p2Ships;
            
            jsAutoPlaceFleet(board, shipsList);
            
            if (gameMode === 'Advanced') {
                const pInv = currentPlacementPlayer === 'P1' ? p1Inventory : p2Inventory;
                let mines = pInv.mine;
                while (mines > 0) {
                    const r = Math.floor(Math.random()*10);
                    const c = Math.floor(Math.random()*10);
                    if (board[r][c] === 0) {
                        board[r][c] = 6;
                        mines--;
                    }
                }
                let pvos = pInv.pvo;
                while (pvos > 0) {
                    const r = Math.floor(Math.random()*10);
                    const c = Math.floor(Math.random()*10);
                    if (board[r][c] === 0) {
                        board[r][c] = 7;
                        pvos--;
                    }
                }
                placedDefenseCount = { mine: 0, pvo: 0 };
            }
            poolShipsPlaced = Array(10).fill(true);
            
            updatePlacementUI();
        }

        function jsAutoPlaceFleet(board, shipsList) {
            for (let r = 0; r < 10; r++) {
                for (let c = 0; c < 10; c++) board[r][c] = 0;
            }
            shipsList.length = 0;
            const sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1];
            
            while (true) {
                let success = true;
                for (let s = 0; s < sizes.length; s++) {
                    const size = sizes[s];
                    let placed = false;
                    for (let attempt = 0; attempt < 1000; attempt++) {
                        const r = Math.floor(Math.random() * 10);
                        const c = Math.floor(Math.random() * 10);
                        const orientation = Math.random() < 0.5 ? 'H' : 'V';
                        
                        let coords = [];
                        if (orientation === 'H') {
                            for (let i = 0; i < size; i++) coords.push([r, c+i]);
                        } else {
                            for (let i = 0; i < size; i++) coords.push([r+i, c]);
                        }
                        
                        if (jsCheckPlacementValid(board, coords)) {
                            coords.forEach(([rc, cc]) => {
                                board[rc][cc] = 1;
                            });
                            shipsList.push({
                                size: size,
                                coords: coords,
                                sunk: false
                            });
                            placed = true;
                            break;
                        }
                    }
                    if (!placed) {
                        // restart
                        for (let r = 0; r < 10; r++) {
                            for (let c = 0; c < 10; c++) board[r][c] = 0;
                        }
                        shipsList.length = 0;
                        success = false;
                        break;
                    }
                }
                if (success) break;
            }
        }

        function finishPlacement() {
            playSketchSound();
            if (playerCount === 2 && currentPlacementPlayer === 'P1') {
                // Transition to Player 2 placements
                setupPlacementPhase('P2');
            } else {
                // Start battle!
                if (playerCount === 1) {
                    // Randomize CPU ships, mines, and PVO
                    jsAutoPlaceFleet(p2Board, p2Ships);
                    let cpuMines = cpuHunter.inventory.mine;
                    while (cpuMines > 0) {
                        const r = Math.floor(Math.random()*10);
                        const c = Math.floor(Math.random()*10);
                        if (p2Board[r][c] === 0) {
                            p2Board[r][c] = 6;
                            cpuMines--;
                        }
                    }
                    let cpuPvos = cpuHunter.inventory.pvo;
                    while (cpuPvos > 0) {
                        const r = Math.floor(Math.random()*10);
                        const c = Math.floor(Math.random()*10);
                        if (p2Board[r][c] === 0) {
                            p2Board[r][c] = 7;
                            cpuPvos--;
                        }
                    }
                }
                
                startBattle();
                if (playerCount === 2) {
                    triggerIntermissionScreen();
                }
            }
        }

        // --- BATTLE CONTROL SYSTEM ---
        let battleLogs = [];

        function startBattle() {
            gamePhase = 'PLAYING';
            currentTurn = 'P1';
            activeWeapon = null;
            battleLogs = ["⚔️ КАРТА СРАЖЕНИЙ: Флоты вышли в море! Огонь!"];
            
            document.getElementById("battleLogsBox").innerHTML = "";
            addLog("📡 Бой начался! Радары активированы.");
            
            renderBattleBoards();
            renderBattleInventories();
            updateBattleHeaders();
            showScreen("screenBattle");
        }

        function updateBattleHeaders() {
            document.getElementById("turnArrow").innerText = currentTurn === 'P1' ? "◀" : "▶";
            
            // Highlight active profile card
            if (currentTurn === 'P1') {
                document.getElementById("profileP1").classList.add("active");
                document.getElementById("profileP2").classList.remove("active");
            } else {
                document.getElementById("profileP1").classList.remove("active");
                document.getElementById("profileP2").classList.add("active");
            }
            
            const lTitle = document.getElementById("titleBoardLeft");
            const rTitle = document.getElementById("titleBoardRight");
            
            if (playerCount === 1) {
                lTitle.innerText = "🛡️ НАШ ФЛОТ";
                rTitle.innerText = "🛰️ РАДАР ПРОТИВНИКА";
            } else {
                lTitle.innerText = currentTurn === 'P1' ? "🛡️ НАШ ФЛОТ" : "🛰️ РАДАР ПРОТИВНИКА";
                rTitle.innerText = currentTurn === 'P1' ? "🛰️ РАДАР ПРОТИВНИКА" : "🛡️ НАШ ФЛОТ";
            }
            
            updateRankHeader();
        }

        function addLog(text) {
            battleLogs.push(text);
            const box = document.getElementById("battleLogsBox");
            const entry = document.createElement("div");
            entry.className = "log-entry";
            entry.innerText = text;
            box.insertBefore(entry, box.firstChild);
        }

        function renderBattleLetters(containerId) {
            const container = document.getElementById(containerId);
            container.innerHTML = "";
            LETTERS.forEach(l => {
                const d = document.createElement("div");
                d.className = "grid-row-header";
                d.innerText = l;
                container.appendChild(d);
            });
        }

        function renderBattleBoards() {
            renderBattleLetters("battleLettersLeft");
            renderBattleLetters("battleLettersRight");
            
            renderBattleNumbers("battleNumbersLeft");
            renderBattleNumbers("battleNumbersRight");
            
            const gridLeft = document.getElementById("boardGridLeft");
            const gridRight = document.getElementById("boardGridRight");
            gridLeft.innerHTML = "";
            gridRight.innerHTML = "";

            const leftBoard = p1Board;
            const rightBoard = p2Board;
            
            const cheatMode = document.getElementById("cheatModeSelect").checked;
            const forceShowShips = (gamePhase === 'GAMEOVER');

            // Left grid (Player 1 Board)
            // In 1-Player mode (vs Bot), Player 1's ships are always shown.
            // In 2-Player mode, Player 1's ships are shown only during P1's turn.
            const showShipsLeft = (playerCount === 1) || (currentTurn === 'P1');
            
            for (let r = 0; r < 10; r++) {
                for (let c = 0; c < 10; c++) {
                    const cell = document.createElement("div");
                    cell.className = "cell";
                    const val = leftBoard[r][c];
                    applyCellGraphics(cell, val, showShipsLeft, cheatMode, forceShowShips);
                    
                    // Left Board is clickable only during P2's turn in 2-Player mode
                    if (playerCount === 2 && currentTurn === 'P2' && gamePhase === 'PLAYING') {
                        cell.onclick = () => onTargetGridClick(r, c);
                    }
                    
                    gridLeft.appendChild(cell);
                }
            }

            // Right grid (Player 2 / CPU Board)
            // Ships are shown only during P2's turn in 2-Player mode.
            const showShipsRight = (playerCount === 2 && currentTurn === 'P2');
            
            for (let r = 0; r < 10; r++) {
                for (let c = 0; c < 10; c++) {
                    const cell = document.createElement("div");
                    cell.className = "cell";
                    const val = rightBoard[r][c];
                    applyCellGraphics(cell, val, showShipsRight, cheatMode, forceShowShips);
                    
                    // Right Board is clickable during P1's turn
                    if (currentTurn === 'P1' && gamePhase === 'PLAYING') {
                        cell.onclick = () => onTargetGridClick(r, c);
                    }
                    
                    gridRight.appendChild(cell);
                }
            }
        }

        function applyCellGraphics(cell, val, showShips, cheatMode, forceShowShips) {
            const reveal = showShips || cheatMode || forceShowShips;
            if (val === 0) {
                cell.innerText = " ";
            } else if (val === 1) { // Ship
                if (reveal) {
                    cell.innerText = "⛵";
                    cell.style.color = "#2B3E90";
                } else {
                    cell.innerText = " ";
                }
            } else if (val === 2) { // Miss
                cell.innerText = "•";
                cell.className = "cell cell-miss";
            } else if (val === 3) { // Hit
                cell.innerText = "💥";
                cell.className = "cell cell-hit";
            } else if (val === 4) { // Sunk
                cell.innerText = "❌";
                cell.className = "cell cell-sunk";
            } else if (val === 5) { // Scanned
                cell.innerText = "⛵";
                cell.className = "cell cell-revealed";
            } else if (val === 6) { // Mine
                if (reveal) {
                    cell.innerText = "💣";
                } else {
                    cell.innerText = " ";
                }
            } else if (val === 7) { // PVO
                if (reveal) {
                    cell.innerText = "🛡️";
                } else {
                    cell.innerText = " ";
                }
            } else if (val === 8) { // Exploded Mine
                cell.innerText = "💥";
                cell.className = "cell cell-hit";
            } else if (val === 9) { // Destroyed PVO
                cell.innerText = "💨";
                cell.style.opacity = 0.5;
            }
        }

        function renderBattleInventories() {
            const leftInv = document.getElementById("battleInvLeft");
            const rightInv = document.getElementById("battleInvRight");
            leftInv.innerHTML = "";
            rightInv.innerHTML = "";

            if (gameMode !== 'Advanced') return;

            const items = ["radar", "torpedo", "bomber"];
            const labels = { radar: "🛰️ Радар", torpedo: "🚀 Торпеда", bomber: "🛩️ Авиаудар" };

            // Left Inventory (always Player 1)
            items.forEach(k => {
                const qty = p1Inventory[k] || 0;
                const d = document.createElement("div");
                d.className = "inv-item";
                
                const isP1Turn = (currentTurn === 'P1' && gamePhase === 'PLAYING');
                if (qty === 0 || !isP1Turn) {
                    d.className += " disabled";
                }
                if (isP1Turn && activeWeapon === k) {
                    d.className += " active";
                }
                d.innerText = labels[k] + " (" + qty + ")";
                
                if (isP1Turn && qty > 0) {
                    d.onclick = () => {
                        selectWeapon(k);
                    };
                }
                leftInv.appendChild(d);
            });

            // Right Inventory (always Player 2 / CPU)
            const p2InvSource = playerCount === 2 ? p2Inventory : cpuHunter.inventory;
            items.forEach(k => {
                const qty = p2InvSource[k] || 0;
                const d = document.createElement("div");
                d.className = "inv-item";
                
                const isP2Turn = (currentTurn === 'P2' && playerCount === 2 && gamePhase === 'PLAYING');
                if (qty === 0 || !isP2Turn) {
                    d.className += " disabled";
                }
                if (isP2Turn && activeWeapon === k) {
                    d.className += " active";
                }
                d.innerText = labels[k] + " (" + qty + ")";
                
                if (isP2Turn && qty > 0) {
                    d.onclick = () => {
                        selectWeapon(k);
                    };
                }
                rightInv.appendChild(d);
            });
        }

        function selectWeapon(w) {
            playSketchSound();
            if (activeWeapon === w) {
                activeWeapon = null;
            } else {
                activeWeapon = w;
            }
            renderBattleInventories();
        }

        // --- ATTACK EXECUTION ---
        function onTargetGridClick(r, c) {
            if (gamePhase !== 'PLAYING') return;
            if (playerCount === 1 && currentTurn !== 'P1') return; // CPU turn is not interactive

            const attacker = currentTurn;
            const targetBoard = attacker === 'P1' ? p2Board : p1Board;
            const targetShips = attacker === 'P1' ? p2Ships : p1Ships;
            const attackerName = attacker === 'P1' ? 'ИГРОК 1' : 'ИГРОК 2';

            // Target already clicked?
            const val = targetBoard[r][c];
            if (activeWeapon === null && [2, 3, 4, 8, 9].includes(val)) return;

            const rowLetter = LETTERS[r];
            const activeInv = attacker === 'P1' ? p1Inventory : p2Inventory;

            if (activeWeapon === null) {
                // 1. Standard single shot
                playShotSound();
                if (attacker === 'P1') {
                    matchStats.p1Shots++;
                } else {
                    matchStats.p2Shots++;
                }
                executeSingleShot(targetBoard, targetShips, r, c, attackerName, attacker);
                
            } else if (activeWeapon === 'radar') {
                activeInv.radar--;
                activeWeapon = null;
                playSketchSound();
                addLog(`🛰️ ${attackerName}: Запущен радар в сектор ${rowLetter}${c+1}.`);
                
                for (let nr = r-1; nr <= r+1; nr++) {
                    for (let nc = c-1; nc <= c+1; nc++) {
                        if (nr >= 0 && nr < 10 && nc >= 0 && nc < 10) {
                            const cv = targetBoard[nr][nc];
                            if (cv === 1) targetBoard[nr][nc] = 5; // Reveal
                            else if (cv === 0) targetBoard[nr][nc] = 2; // Miss
                        }
                    }
                }
                playPvoSound();
                showToast("Сектор просканирован радаром!", "🛰️");
                renderBattleBoards();
                renderBattleInventories();
                
            } else if (activeWeapon === 'bomber') {
                activeInv.bomber--;
                activeWeapon = null;
                triggerAirStrikeAnimation(r, c, attacker);
                
            } else if (activeWeapon === 'torpedo') {
                activeInv.torpedo--;
                activeWeapon = null;
                triggerTorpedoAnimation(r, attacker);
            }
        }

        function renderBattleNumbers(containerId) {
            const container = document.getElementById(containerId);
            if (!container) return;
            container.innerHTML = "";
            for (let i = 1; i <= 10; i++) {
                const d = document.createElement("div");
                d.innerText = i;
                container.appendChild(d);
            }
        }

        function markNeighborsAsMiss(board, coords) {
            coords.forEach(([r, c]) => {
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        const nr = r + dr;
                        const nc = c + dc;
                        if (nr >= 0 && nr < 10 && nc >= 0 && nc < 10) {
                            if (board[nr][nc] === 0) {
                                board[nr][nc] = 2; // Mark as Miss
                            }
                        }
                    }
                }
            });
        }

        function executeSingleShot(board, shipsList, r, c, attackerName, attackerId) {
            const cellVal = board[r][c];
            const letter = LETTERS[r];
            
            if (cellVal === 1 || cellVal === 5) {
                // Hit ship cell!
                board[r][c] = 3;
                if (attackerId === 'P1') matchStats.p1Hits++;
                else matchStats.p2Hits++;

                // Locate ship
                let hitShip = null;
                shipsList.forEach(s => {
                    s.coords.forEach(([sr, sc]) => {
                        if (sr === r && sc === c) hitShip = s;
                    });
                });

                // Check if sunk
                const isSunk = hitShip.coords.every(([sr, sc]) => board[sr][sc] === 3);
                
                if (isSunk) {
                    hitShip.sunk = true;
                    hitShip.coords.forEach(([sr, sc]) => {
                        board[sr][sc] = 4; // Mark Sunk
                    });
                    markNeighborsAsMiss(board, hitShip.coords);
                    
                    playSunkSound();
                    addLog(`💥 ${attackerName}: Потоплен ${hitShip.size}-палубный корабль в координате ${letter}${c+1}!`);
                    showToast("Потоплен!", "💥");
                    
                    // Earn money in advanced mode
                    if (gameMode === 'Advanced') {
                        const reward = 300 + 100 * hitShip.size;
                        stats[attackerId].xp += reward;
                        addLog(`💰 ${attackerName}: Получен боевой опыт +${reward} XP.`);
                    }
                } else {
                    playExplosionSound();
                    addLog(`🔥 ${attackerName}: Попадание в корабль в координате ${letter}${c+1}!`);
                    showToast("Попадание!", "🔥");
                    if (gameMode === 'Advanced') {
                        stats[attackerId].xp += 150;
                    }
                }

                // Check win condition
                if (shipsList.every(s => s.sunk)) {
                    finishGame(attackerId);
                    return;
                }

                // Turn remains attacker's
                renderBattleBoards();
                renderBattleInventories();
                
                // If bot hit, bot shoots again
                if (!['АВИАУДАР', 'ТОРПЕДА', 'МИНА'].includes(attackerName)) {
                    if (attackerId === 'P2' && playerCount === 1 && gamePhase === 'PLAYING') {
                        setTimeout(runCpuTurnLogic, 900);
                    }
                }

            } else if (cellVal === 0) {
                // Miss
                board[r][c] = 2; // miss
                playMissSound();
                addLog(`💧 ${attackerName}: Промах в координате ${letter}${c+1}.`);
                
                renderBattleBoards();
                renderBattleInventories();
                
                // Change turn
                if (!['АВИАУДАР', 'ТОРПЕДА', 'МИНА'].includes(attackerName)) {
                    changeTurnSequence();
                }

            } else if (cellVal === 6) {
                // Mine hit!
                board[r][c] = 8; // exploded mine
                playExplosionSound();
                addLog(`💥 БУМ! ${attackerName} подорвался на вражеской МИНЕ в координате ${letter}${c+1}!`);
                showToast("Подорвались на мине противника!", "💣");
                
                // Counter strike to attacker
                const defenderBoard = attackerId === 'P1' ? p1Board : p2Board;
                const defenderId = attackerId === 'P1' ? 'P2' : 'P1';
                
                let available = [];
                for (let pr = 0; pr < 10; pr++) {
                    for (let pc = 0; pc < 10; pc++) {
                        if ([0, 1, 6, 7].includes(defenderBoard[pr][pc])) {
                            available.push([pr, pc]);
                        }
                    }
                }
                if (available.length > 0) {
                    const [pr, pc] = available[Math.floor(Math.random() * available.length)];
                    addLog(`⚡ Детонация: мина бьет в ответ по полю ${attackerName}!`);
                    
                    // Run shot on attacker's board
                    if (attackerId === 'P1') {
                        executeSingleShot(p1Board, p1Ships, pr, pc, 'МИНА', 'P2');
                    } else {
                        executeSingleShot(p2Board, p2Ships, pr, pc, 'МИНА', 'P1');
                    }
                }
                
                renderBattleBoards();
                renderBattleInventories();
                
                // Change turn
                changeTurnSequence();

            } else if (cellVal === 7) {
                // Active Air defense hit
                board[r][c] = 9; // destroyed PVO
                playExplosionSound();
                addLog(`🎯 ${attackerName}: Разрушена установка ПВО противника в координате ${letter}${c+1}!`);
                showToast("ПВО снесено!", "🛡️");
                
                renderBattleBoards();
                renderBattleInventories();
                
                // Change turn
                if (!['АВИАУДАР', 'ТОРПЕДА', 'МИНА'].includes(attackerName)) {
                    changeTurnSequence();
                }
            }
        }

        function changeTurnSequence() {
            currentTurn = currentTurn === 'P1' ? 'P2' : 'P1';
            updateBattleHeaders();
            
            if (playerCount === 2 && gamePhase === 'PLAYING') {
                triggerIntermissionScreen();
            } else if (playerCount === 1 && gamePhase === 'PLAYING') {
                renderBattleBoards();
                renderBattleInventories();
                if (currentTurn === 'P2') {
                    setTimeout(runCpuTurnLogic, 1000);
                }
            }
        }

        // --- ANIMATIONS ---
        function triggerAirStrikeAnimation(r, c, attackerId) {
            const overlay = document.getElementById("animOverlay");
            overlay.style.display = "block";
            
            const plane = document.getElementById("animPlane");
            const shadow = document.getElementById("animPlaneShadow");
            
            // Reset position
            plane.style.transition = "none";
            shadow.style.transition = "none";
            
            if (attackerId === 'P1') {
                plane.style.top = "-120px";
                plane.style.left = "-120px";
                plane.style.transform = "none";
                shadow.style.top = "-100px";
                shadow.style.left = "-100px";
                shadow.style.transform = "none";
            } else {
                plane.style.top = "-120px";
                plane.style.left = "100%";
                plane.style.transform = "scaleX(-1)";
                shadow.style.top = "-100px";
                shadow.style.left = "100%";
                shadow.style.transform = "scaleX(-1)";
            }
            
            // Force redraw
            plane.offsetHeight; 
            
            // Start flight
            plane.style.transition = "all 1.6s linear";
            shadow.style.transition = "all 1.6s linear";
            
            if (attackerId === 'P1') {
                plane.style.top = "100%";
                plane.style.left = "100%";
                shadow.style.top = "100%";
                shadow.style.left = "100%";
            } else {
                plane.style.top = "100%";
                plane.style.left = "-120px";
                shadow.style.top = "100%";
                shadow.style.left = "-100px";
            }
            
            playShotSound(); // plane roar whoosh
            
            setTimeout(() => {
                overlay.style.display = "none";
                executeAirStrikeDamage(r, c, attackerId);
            }, 1600);
        }

        function executeAirStrikeDamage(r, c, attackerId) {
            const targetBoard = attackerId === 'P1' ? p2Board : p1Board;
            const targetShips = attackerId === 'P1' ? p2Ships : p1Ships;
            const attackerName = attackerId === 'P1' ? 'ИГРОК 1' : (playerCount === 2 ? 'ИГРОК 2' : 'БОТ');
            
            const letter = LETTERS[r];
            
            // Check Air defense (ПВО) value 7
            let pvoActive = false;
            let pvoR = -1, pvoC = -1;
            for (let tr = 0; tr < 10; tr++) {
                for (let tc = 0; tc < 10; tc++) {
                    if (targetBoard[tr][tc] === 7) {
                        pvoActive = true;
                        pvoR = tr;
                        pvoC = tc;
                        break;
                    }
                }
                if (pvoActive) break;
            }
            
            if (pvoActive) {
                targetBoard[pvoR][pvoC] = 9; // Destroyed
                playPvoSound();
                addLog(`🛡️ ПВО ПРОТИВНИКА: Батарея сбила вражеский самолет! Урон не нанесен.`);
                showToast("Авиаудар перехвачен ПВО противника!", "🛡️");
            } else {
                playExplosionSound();
                addLog(`🚨 АВИАУДАР: Бомбы упали на сектор ${letter}${c+1}!`);
                
                for (let nr = r-1; nr <= r+1; nr++) {
                    for (let nc = c-1; nc <= c+1; nc++) {
                        if (nr >= 0 && nr < 10 && nc >= 0 && nc < 10) {
                            const cv = targetBoard[nr][nc];
                            if ([0, 1, 5, 6, 7].includes(cv)) {
                                executeSingleShot(targetBoard, targetShips, nr, nc, 'АВИАУДАР', attackerId);
                            }
                        }
                    }
                }
            }
            
            // Air Strike ends turn
            changeTurnSequence();
        }

        function triggerTorpedoAnimation(r, attackerId) {
            const overlay = document.getElementById("animOverlay");
            overlay.style.display = "block";
            
            const torpedo = document.getElementById("animTorpedo");
            torpedo.style.transition = "none";
            
            if (attackerId === 'P1') {
                torpedo.style.left = "-80px";
                torpedo.style.transform = "none";
            } else {
                torpedo.style.left = "100%";
                torpedo.style.transform = "scaleX(-1)";
            }
            torpedo.style.top = (45 + r * 34) + "px"; // align to grid row r
            
            torpedo.offsetHeight; // redraw
            
            torpedo.style.transition = "all 0.8s ease-in";
            if (attackerId === 'P1') {
                torpedo.style.left = "100%";
            } else {
                torpedo.style.left = "-80px";
            }
            
            playShotSound();
            
            setTimeout(() => {
                overlay.style.display = "none";
                executeTorpedoDamage(r, attackerId);
            }, 800);
        }

        function executeTorpedoDamage(r, attackerId) {
            const targetBoard = attackerId === 'P1' ? p2Board : p1Board;
            const targetShips = attackerId === 'P1' ? p2Ships : p1Ships;
            const attackerName = attackerId === 'P1' ? 'ИГРОК 1' : (playerCount === 2 ? 'ИГРОК 2' : 'БОТ');
            
            const letter = LETTERS[r];
            let hitSomething = false;
            
            for (let tc = 0; tc < 10; tc++) {
                const cv = targetBoard[r][tc];
                if (cv === 1 || cv === 5) {
                    addLog(`🚀 ТОРПЕДА: Поражен корабль в координате ${letter}${tc+1}!`);
                    executeSingleShot(targetBoard, targetShips, r, tc, 'ТОРПЕДА', attackerId);
                    hitSomething = true;
                    break;
                } else if (cv === 6) {
                    targetBoard[r][tc] = 8;
                    playExplosionSound();
                    addLog(`💥 ТОРПЕДА: Детонация мины в ячейке ${letter}${tc+1}!`);
                    showToast("Мина взорвана торпедой!", "💣");
                    // Mine back-strike
                    const defenderBoard = attackerId === 'P1' ? p1Board : p2Board;
                    let available = [];
                    for (let pr = 0; pr < 10; pr++) {
                        for (let pc = 0; pc < 10; pc++) {
                            if ([0, 1, 6, 7].includes(defenderBoard[pr][pc])) available.push([pr, pc]);
                        }
                    }
                    if (available.length > 0) {
                        const [pr, pc] = available[Math.floor(Math.random()*available.length)];
                        executeSingleShot(defenderBoard, (attackerId==='P1'?p1Ships:p2Ships), pr, pc, 'МИНА', (attackerId==='P1'?'P2':'P1'));
                    }
                    hitSomething = true;
                    break;
                } else if (cv === 7) {
                    targetBoard[r][tc] = 9;
                    playExplosionSound();
                    addLog(`🎯 ТОРПЕДА: Батарея ПВО снесена в ячейке ${letter}${tc+1}!`);
                    showToast("ПВО снесено торпедой!", "🛡️");
                    hitSomething = true;
                    break;
                }
            }
            
            if (!hitSomething) {
                if (targetBoard[r][9] === 0) targetBoard[r][9] = 2;
                playMissSound();
                addLog(`🌊 ТОРПЕДА: Торпеда не встретила целей на ряду ${letter}.`);
            }
            
            changeTurnSequence();
        }

        // --- INTERMISSION SCREEN (Hotseat) ---
        function triggerIntermissionScreen() {
            const overlay = document.getElementById("intermissionOverlay");
            document.getElementById("interTitle").innerText = currentTurn === 'P1' ? "ХОД ИГРОКА 1" : "ХОД ИГРОКА 2";
            document.getElementById("interDesc").innerText = currentTurn === 'P1' ? "Передайте устройство Игроку 1 (captainboom)" : "Передайте устройство Игроку 2";
            overlay.classList.add("active");
            playPvoSound();
        }

        function endIntermission() {
            playSketchSound();
            document.getElementById("intermissionOverlay").classList.remove("active");
            renderBattleBoards();
            renderBattleInventories();
        }

        // --- SMART CPU AI ACTION ---
        function runCpuTurnLogic() {
            if (currentTurn !== 'P2' || gamePhase !== 'PLAYING') return;
            
            // CPU decides to use Air Strike
            if (gameMode === 'Advanced' && cpuHunter.inventory.bomber > 0 && Math.random() < 0.25) {
                cpuHunter.inventory.bomber--;
                
                let tr = 4, tc = 4;
                if (cpuHunter.hits.length > 0) {
                    [tr, tc] = cpuHunter.hits[cpuHunter.hits.length - 1];
                } else {
                    let available = [];
                    for (let r=0; r<10; r++) {
                        for (let c=0; c<10; c++) {
                            if ([0, 1, 6, 7].includes(p1Board[r][c])) available.push([r, c]);
                        }
                    }
                    if (available.length > 0) [tr, tc] = available[Math.floor(Math.random()*available.length)];
                }
                
                addLog(`🛩️ БОТ: Вызван Авиаудар (3x3)!`);
                triggerAirStrikeAnimation(tr, tc, 'P2');
                return;
            }
            
            // CPU decides to use Torpedo
            if (gameMode === 'Advanced' && cpuHunter.inventory.torpedo > 0 && Math.random() < 0.2 && cpuHunter.hits.length > 0) {
                cpuHunter.inventory.torpedo--;
                const tr = cpuHunter.hits[0][0];
                addLog(`🚀 БОТ: Запуск Торпеды по ряду ${LETTERS[tr]}!`);
                triggerTorpedoAnimation(tr, 'P2');
                return;
            }
            
            // Standard smart shot
            const [r, c] = getCpuShot();
            matchStats.p2Shots++;
            
            // CPU Shot logic
            const val = p1Board[r][c];
            if (val === 1) {
                cpuHunter.hits.push([r, c]);
                cpuHunter.state = 'target';
            }
            
            executeSingleShot(p1Board, p1Ships, r, c, 'БОТ', 'P2');
        }

        function getCpuShot() {
            let available_cells = [];
            for (let r = 0; r < 10; r++) {
                for (let c = 0; c < 10; c++) {
                    const val = p1Board[r][c];
                    if ([0, 1, 6, 7].includes(val)) {
                        available_cells.push([r, c]);
                    }
                }
            }
            
            if (available_cells.length === 0) {
                return [0, 0];
            }
            
            const difficultySelect = document.getElementById("difficultySelect");
            const difficulty = difficultySelect ? difficultySelect.value : "Smart";
            
            if (difficulty === "Easy" || cpuHunter.state === "hunt" || cpuHunter.hits.length === 0) {
                return available_cells[Math.floor(Math.random() * available_cells.length)];
            }
            
            // Smart Target mode
            const hits = cpuHunter.hits;
            if (hits.length === 1) {
                const [hr, hc] = hits[0];
                const candidates = [[hr-1, hc], [hr+1, hc], [hr, hc-1], [hr, hc+1]];
                const valid_candidates = candidates.filter(([r, c]) => {
                    return r >= 0 && r < 10 && c >= 0 && c < 10 && [0, 1, 6, 7].includes(p1Board[r][c]);
                });
                if (valid_candidates.length > 0) {
                    return valid_candidates[Math.floor(Math.random() * valid_candidates.length)];
                } else {
                    cpuHunter.state = "hunt";
                    cpuHunter.hits = [];
                    return available_cells[Math.floor(Math.random() * available_cells.length)];
                }
            }
            
            // 2+ hits: orientation known
            let candidates = [];
            if (hits[0][0] === hits[1][0]) {
                const row = hits[0][0];
                const cols = hits.map(h => h[1]);
                const c_min = Math.min(...cols);
                const c_max = Math.max(...cols);
                candidates = [[row, c_min - 1], [row, c_max + 1]];
            } else {
                const col = hits[0][1];
                const rows = hits.map(h => h[0]);
                const r_min = Math.min(...rows);
                const r_max = Math.max(...rows);
                candidates = [[r_min - 1, col], [r_max + 1, col]];
            }
            
            const valid_candidates = candidates.filter(([r, c]) => {
                return r >= 0 && r < 10 && c >= 0 && c < 10 && [0, 1, 6, 7].includes(p1Board[r][c]);
            });
            
            if (valid_candidates.length > 0) {
                return valid_candidates[Math.floor(Math.random() * valid_candidates.length)];
            } else {
                let adj_candidates = [];
                hits.forEach(([hr, hc]) => {
                    [[hr-1, hc], [hr+1, hc], [hr, hc-1], [hr, hc+1]].forEach(([r, c]) => {
                        if (r >= 0 && r < 10 && c >= 0 && c < 10 && [0, 1, 6, 7].includes(p1Board[r][c])) {
                            adj_candidates.push([r, c]);
                        }
                    });
                });
                if (adj_candidates.length > 0) {
                    return adj_candidates[Math.floor(Math.random() * adj_candidates.length)];
                } else {
                    cpuHunter.state = "hunt";
                    cpuHunter.hits = [];
                    return available_cells[Math.floor(Math.random() * available_cells.length)];
                }
            }
        }

        // --- GAME OVER SCREEN CONTROLLER ---
        function finishGame(winnerId) {
            gamePhase = 'GAMEOVER';
            
            const goTitle = document.getElementById("goTitle");
            const goDesc = document.getElementById("goDesc");
            const goStats = document.getElementById("goStats");
            
            if (winnerId === 'P1') {
                playVictorySound();
                goTitle.innerText = "ПОБЕДА! 🏆";
                goTitle.className = "go-title win";
                goDesc.innerText = playerCount === 2 ? "Игрок 1 полностью разбил флот Игрока 2!" : "Вы полностью ликвидировали эскадру bestie!";
                stats.P1.xp += 1000;
                stats.P1.wins++;
                saveProfile();
            } else {
                playDefeatSound();
                goTitle.innerText = "ПОРАЖЕНИЕ 💀";
                goTitle.className = "go-title lose";
                goDesc.innerText = playerCount === 2 ? "Игрок 2 полностью разбил ваш флот!" : "Компьютер полностью уничтожил ваш флот.";
                stats.P1.xp += 150;
                stats.P1.losses++;
                saveProfile();
            }
            let statsText = "";
            if (playerCount === 2) {
                const p1Acc = matchStats.p1Shots > 0 ? Math.round((matchStats.p1Hits / matchStats.p1Shots) * 100) : 0;
                const p2Acc = matchStats.p2Shots > 0 ? Math.round((matchStats.p2Hits / matchStats.p2Shots) * 100) : 0;
                statsText = `Игрок 1: снарядов ${matchStats.p1Shots}, меткость ${p1Acc}% | Игрок 2: снарядов ${matchStats.p2Shots}, меткость ${p2Acc}%`;
            } else {
                const p1Acc = matchStats.p1Shots > 0 ? Math.round((matchStats.p1Hits / matchStats.p1Shots) * 100) : 0;
                statsText = `Снарядов израсходовано: ${matchStats.p1Shots} | Меткость: ${p1Acc}%`;
            }
            goStats.innerText = statsText;
            
            // Reveal boards final values
            renderBattleBoards();
            
            showScreen("screenGameOver");
        }

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && isDragging) {
                e.preventDefault();
                placementOrientation = placementOrientation === 'H' ? 'V' : 'H';
                updatePlacementOrientationUI();
                updateGhostOrientation();
            }
        });

        // Page load initialization
        loadProfile();

    </script>
</body>
</html>
"""

# Render the custom component inside Streamlit layout
components.html(html_code, height=950, scrolling=False)
