import streamlit as st

def load_veles_design_system():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0F172A;
        color: #E5E7EB;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1E293B;
    }

    .veles-page-title {
        font-size: 36px;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 6px;
    }

    .veles-page-subtitle {
        font-size: 16px;
        color: #94A3B8;
        margin-bottom: 28px;
    }

    .veles-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        margin-bottom: 18px;
    }

    .veles-metric-label {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 500;
    }

    .veles-metric-value {
        color: #F8FAFC;
        font-size: 34px;
        font-weight: 800;
        margin-top: 10px;
    }

    .veles-metric-change-positive {
        color: #10B981;
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
    }

    .veles-metric-change-negative {
        color: #EF4444;
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
    }

    .veles-insight-title {
        color: #3B82F6;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }

    .veles-insight-text {
        color: #E5E7EB;
        font-size: 16px;
        line-height: 1.6;
    }

    .veles-company-name {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .veles-company-meta {
        color: #94A3B8;
        font-size: 14px;
        margin-bottom: 12px;
    }

    .veles-button-link {
        color: #3B82F6;
        font-size: 14px;
        font-weight: 700;
    }
    
    .veles-workflow-shell {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 22px;
        padding: 18px 20px;
        margin-bottom: 22px;
        box-shadow: 0 20px 45px rgba(0,0,0,0.22);
        backdrop-filter: blur(14px);
    }

    .veles-workflow-topline {
        display: flex;
        justify-content: space-between;
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .veles-workflow-progress-bg {
        height: 8px;
        width: 100%;
        border-radius: 999px;
        background: rgba(51, 65, 85, 0.9);
        overflow: hidden;
    }

    .veles-workflow-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563EB, #06B6D4);
        transition: width 0.35s ease;
    }

    .veles-workflow-card {
        min-height: 92px;
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 18px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        background: rgba(15, 23, 42, 0.72);
        box-shadow: 0 12px 30px rgba(0,0,0,0.20);
        backdrop-filter: blur(12px);
    }

    .veles-workflow-card-active {
        border-color: rgba(59, 130, 246, 0.85);
        box-shadow: 0 0 0 1px rgba(59,130,246,0.35), 0 18px 45px rgba(37,99,235,0.20);
    }

    .veles-workflow-card-done {
        border-color: rgba(16, 185, 129, 0.5);
        background: rgba(6, 78, 59, 0.20);
    }

    .veles-workflow-card-pending {
        opacity: 0.68;
    }

    .veles-workflow-status {
        font-size: 20px;
        font-weight: 900;
        color: #38BDF8;
        margin-bottom: 8px;
    }

    .veles-workflow-title {
        color: #F8FAFC;
        font-size: 15px;
        font-weight: 800;
    }

    
    .veles-glass-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.24);
        backdrop-filter: blur(14px);
    }

    .veles-card-eyebrow {
        color: #38BDF8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .veles-card-title {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .veles-card-body {
        color: #CBD5E1;
        font-size: 15px;
        line-height: 1.65;
    }

    .veles-kpi-card {
        background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(15,23,42,0.70));
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.25);
        backdrop-filter: blur(14px);
    }

    .veles-kpi-label {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .veles-kpi-value {
        color: #F8FAFC;
        font-size: 34px;
        font-weight: 900;
        margin-top: 10px;
    }

    .veles-kpi-positive {
        color: #10B981;
        font-size: 13px;
        font-weight: 700;
        margin-top: 8px;
    }

    .veles-kpi-negative {
        color: #EF4444;
        font-size: 13px;
        font-weight: 700;
        margin-top: 8px;
    }

    
    .veles-panel-header {
        margin-top: 26px;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.18);
    }

    .veles-panel-title {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 850;
        letter-spacing: -0.02em;
    }

    .veles-panel-subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 6px;
        line-height: 1.5;
    }

    
    .veles-sticky-workflow {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 22px;
        padding: 16px 18px;
        margin-bottom: 22px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.28);
        backdrop-filter: blur(16px);
    }

    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.14);
    }

    .veles-sidebar-brand {
        padding: 8px 4px 26px 4px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.16);
        margin-bottom: 22px;
    }

    .veles-sidebar-logo {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .veles-sidebar-subtitle {
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.45;
        max-width: 210px;
    }

    .veles-nav-section-label {
        color: #64748B;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 20px 0 8px 4px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        color: #CBD5E1;
        border: 1px solid transparent;
        border-radius: 14px;
        justify-content: flex-start;
        font-weight: 700;
        padding: 10px 12px;
        margin-bottom: 2px;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59, 130, 246, 0.10);
        border-color: rgba(59, 130, 246, 0.22);
        color: #F8FAFC;
    }

    .veles-sidebar-user-card {
        margin-top: 34px;
        padding: 16px;
        border-radius: 18px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 14px 32px rgba(0,0,0,0.22);
    }

    .veles-user-name {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .veles-user-role {
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.45;
    }

    
    .veles-nav-active-label {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #F8FAFC;
        background: rgba(59, 130, 246, 0.14);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-left: 3px solid #38BDF8;
        border-radius: 14px;
        padding: 10px 12px;
        margin: 4px 0 2px 0;
        font-size: 14px;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(37, 99, 235, 0.18);
    }

    .veles-nav-inactive-label {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #CBD5E1;
        padding: 10px 12px;
        margin: 4px 0 2px 0;
        font-size: 14px;
        font-weight: 700;
    }

    .veles-nav-icon {
        width: 18px;
        display: inline-block;
        color: #38BDF8;
    }

    
    .veles-nav-current {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #F8FAFC;
        background: rgba(59, 130, 246, 0.14);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-left: 3px solid #38BDF8;
        border-radius: 14px;
        padding: 10px 12px;
        margin: 4px 0 6px 0;
        font-size: 14px;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(37, 99, 235, 0.18);
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        color: #CBD5E1;
        border: 1px solid transparent;
        border-radius: 14px;
        justify-content: flex-start;
        font-weight: 700;
        padding: 10px 12px;
        margin-bottom: 4px;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59, 130, 246, 0.10);
        border-color: rgba(59, 130, 246, 0.22);
        color: #F8FAFC;
    }

    
    .veles-login-shell {
        max-width: 980px;
        margin: 7vh auto 28px auto;
        text-align: center;
    }

    .veles-login-brand {
        color: #38BDF8;
        font-size: 14px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .veles-login-title {
        color: #F8FAFC;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-bottom: 10px;
    }

    .veles-login-subtitle {
        color: #94A3B8;
        font-size: 16px;
        line-height: 1.6;
        max-width: 680px;
        margin: 0 auto;
    }

    .veles-login-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 26px;
        padding: 28px;
        box-shadow: 0 22px 55px rgba(0,0,0,0.30);
        backdrop-filter: blur(16px);
    }

    .veles-login-info-card {
        background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(30,41,59,0.74));
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-radius: 26px;
        padding: 30px;
        box-shadow: 0 22px 55px rgba(0,0,0,0.30);
        color: #CBD5E1;
        min-height: 300px;
    }

    .veles-login-info-title {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 850;
        margin-bottom: 18px;
    }

    .veles-login-info-card li {
        margin-bottom: 12px;
        line-height: 1.5;
    }

    
    .veles-auth-page {
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        background:
            radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.22), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(14, 165, 233, 0.18), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(16, 185, 129, 0.10), transparent 28%),
            linear-gradient(135deg, #020617 0%, #0B1120 45%, #020617 100%);
    }

    .veles-auth-bg-grid {
        position: absolute;
        inset: 0;
        opacity: 0.22;
        background-image:
            linear-gradient(rgba(148,163,184,0.12) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,0.12) 1px, transparent 1px);
        background-size: 54px 54px;
        mask-image: radial-gradient(circle at center, black, transparent 72%);
    }

    .veles-auth-page:before,
    .veles-auth-page:after {
        content: "";
        position: absolute;
        width: 42vw;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(56,189,248,0.38), transparent);
        top: 24%;
    }

    .veles-auth-page:before {
        left: 0;
        transform: rotate(18deg);
    }

    .veles-auth-page:after {
        right: 0;
        transform: rotate(-18deg);
    }

    .veles-auth-orb {
        position: absolute;
        width: 420px;
        height: 420px;
        border-radius: 999px;
        filter: blur(80px);
        opacity: 0.22;
        animation: velesFloat 8s ease-in-out infinite alternate;
    }

    .veles-auth-orb-left {
        left: -140px;
        bottom: 10%;
        background: #2563EB;
    }

    .veles-auth-orb-right {
        right: -140px;
        top: 8%;
        background: #06B6D4;
        animation-delay: 1.2s;
    }

    @keyframes velesFloat {
        from { transform: translateY(0px) scale(1); }
        to { transform: translateY(-28px) scale(1.04); }
    }

    .veles-auth-shell {
        position: relative;
        max-width: 1180px;
        margin: 9vh auto 0 auto;
        padding: 0 32px;
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        gap: 56px;
        align-items: center;
    }

    .veles-auth-hero {
        padding: 34px 0;
    }

    .veles-auth-kicker {
        color: #38BDF8;
        font-size: 13px;
        font-weight: 950;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 22px;
    }

    .veles-auth-title {
        color: #F8FAFC;
        font-size: clamp(42px, 5vw, 72px);
        line-height: 0.96;
        font-weight: 950;
        letter-spacing: -0.065em;
        max-width: 760px;
        margin-bottom: 24px;
    }

    .veles-auth-subtitle {
        color: #94A3B8;
        font-size: 17px;
        line-height: 1.75;
        max-width: 660px;
        margin-bottom: 34px;
    }

    .veles-auth-feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        max-width: 650px;
    }

    .veles-auth-feature {
        color: #CBD5E1;
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 13px 14px;
        font-size: 13px;
        font-weight: 800;
        backdrop-filter: blur(12px);
    }

    .veles-auth-card-wrap {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 30px;
        padding: 26px;
        box-shadow: 0 28px 70px rgba(0,0,0,0.42);
        backdrop-filter: blur(18px);
    }

    .veles-auth-card-header {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .veles-auth-logo-mark {
        width: 54px;
        height: 54px;
        display: grid;
        place-items: center;
        border-radius: 18px;
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 950;
        background: linear-gradient(135deg, #2563EB, #06B6D4);
        box-shadow: 0 18px 38px rgba(37, 99, 235, 0.28);
    }

    .veles-auth-card-title {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: -0.04em;
    }

    .veles-auth-card-caption {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 3px;
    }

    .veles-auth-form-card {
        position: relative;
        margin-top: 0;
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 30px;
        padding: 28px;
        box-shadow: 0 28px 70px rgba(0,0,0,0.42);
        backdrop-filter: blur(18px);
    }

    .veles-auth-footnote {
        margin-top: 18px;
        color: #64748B;
        font-size: 12px;
        text-align: center;
        line-height: 1.5;
    }

    .veles-auth-form-card .stButton > button {
        background: linear-gradient(90deg, #2563EB, #06B6D4);
        color: white;
        border: 0;
        border-radius: 14px;
        font-weight: 900;
        height: 48px;
        box-shadow: 0 18px 36px rgba(37,99,235,0.28);
    }

    .veles-auth-form-card .stTextInput input {
        background: rgba(2, 6, 23, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 14px;
        color: #F8FAFC;
    }

    .veles-auth-form-card [data-testid="stRadio"] label {
        color: #CBD5E1;
    }

    @media (max-width: 980px) {
        .veles-auth-shell {
            grid-template-columns: 1fr;
            margin-top: 4vh;
            gap: 24px;
        }

        .veles-auth-feature-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .veles-auth-form-card {
            margin-top: 20px;
            padding-top: 28px;
        }
    }

    
    .veles-auth-background {
        position: fixed;
        inset: 0;
        z-index: -1;
        overflow: hidden;
        background:
            radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.22), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(14, 165, 233, 0.18), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(16, 185, 129, 0.10), transparent 28%),
            linear-gradient(135deg, #020617 0%, #0B1120 45%, #020617 100%);
    }

    .veles-auth-spacer {
        height: 8vh;
    }

    .veles-auth-hero-panel {
        padding: 32px 12px;
    }

    .veles-auth-card-header-only {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 30px 30px 0 0;
        padding: 28px 28px 8px 28px;
        box-shadow: 0 20px 55px rgba(0,0,0,0.30);
        backdrop-filter: blur(18px);
        display: flex;
        gap: 16px;
        align-items: center;
    }

    .veles-auth-card-header-only + div {
        background: rgba(15, 23, 42, 0.78);
        border-left: 1px solid rgba(148, 163, 184, 0.22);
        border-right: 1px solid rgba(148, 163, 184, 0.22);
        padding: 10px 28px 0 28px;
        backdrop-filter: blur(18px);
    }

    
    /* Auth glass card refinement */
    .veles-auth-card-header-only {
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-bottom: 0;
        border-radius: 30px 30px 0 0;
        padding: 32px 32px 16px 32px;
        box-shadow:
            0 28px 80px rgba(0,0,0,0.45),
            0 0 70px rgba(37,99,235,0.16);
        backdrop-filter: blur(24px);
        display: flex;
        gap: 18px;
        align-items: center;
    }

    .veles-auth-card-header-only + div {
        background: rgba(15, 23, 42, 0.62);
        border-left: 1px solid rgba(148, 163, 184, 0.24);
        border-right: 1px solid rgba(148, 163, 184, 0.24);
        border-bottom: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 0 0 30px 30px;
        padding: 12px 32px 32px 32px;
        backdrop-filter: blur(24px);
        box-shadow:
            0 28px 80px rgba(0,0,0,0.45),
            0 0 70px rgba(37,99,235,0.16);
    }

    .veles-auth-card-title {
        font-size: 34px;
        font-weight: 950;
        letter-spacing: -0.055em;
    }

    .veles-auth-card-caption {
        color: #94A3B8;
        font-size: 15px;
        margin-top: 4px;
    }

    .veles-auth-logo-mark {
        width: 62px;
        height: 62px;
        border-radius: 20px;
        font-size: 32px;
        background: linear-gradient(135deg, #2563EB, #06B6D4);
        box-shadow:
            0 18px 44px rgba(37,99,235,0.36),
            inset 0 0 18px rgba(255,255,255,0.16);
    }

    .veles-auth-spacer {
        height: 5vh;
    }

    
    /* Final auth single-card shell */
    div[data-testid="column"]:has(.veles-auth-card-header-only) {
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 32px;
        padding: 34px 34px 32px 34px;
        box-shadow:
            0 30px 90px rgba(0,0,0,0.50),
            0 0 80px rgba(37,99,235,0.18);
        backdrop-filter: blur(26px);
    }

    .veles-auth-card-header-only {
        background: transparent;
        border: 0;
        border-radius: 0;
        padding: 0 0 24px 0;
        box-shadow: none;
        backdrop-filter: none;
        display: flex;
        gap: 18px;
        align-items: center;
        border-bottom: 1px solid rgba(148, 163, 184, 0.18);
        margin-bottom: 18px;
    }

    .veles-auth-card-header-only + div {
        background: transparent;
        border: 0;
        border-radius: 0;
        padding: 0;
        backdrop-filter: none;
        box-shadow: none;
    }

    
    /* Auth card vertical alignment */
    div[data-testid="column"]:has(.veles-auth-card-header-only) {
        margin-top: 58px;
    }

    
    /* Final login polish */
    .veles-auth-title {
        max-width: 720px;
    }

    .veles-auth-subtitle {
        max-width: 620px;
        margin-bottom: 22px;
    }

    .veles-auth-feature-grid {
        margin-top: 0;
    }

    #MainMenu {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    [data-testid="stDecoration"] {
        display: none;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
    }

    
    /* Equalize login card with hero */
    div[data-testid="column"]:has(.veles-auth-card-header-only) {
        margin-top: 95px;
    }

    
    /* Remove Streamlit chrome */
    #MainMenu {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    [data-testid="stDecoration"] {
        display: none;
    }

    footer {
        visibility: hidden;
    }

    
    /* Navigation redesign sprint */
    [data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 20% 0%, rgba(37, 99, 235, 0.18), transparent 34%),
            linear-gradient(180deg, #020617 0%, #07111F 52%, #020617 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.14);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 28px;
    }

    .veles-sidebar-brand {
        padding: 18px 16px 20px 16px;
        margin-bottom: 18px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.14);
    }

    .veles-sidebar-logo {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 950;
        letter-spacing: 0.08em;
    }

    .veles-sidebar-subtitle {
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.4;
        margin-top: 6px;
    }

    .veles-nav-section-label {
        color: #64748B;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 20px 10px 8px 10px;
    }

    .veles-nav-current {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 4px 4px;
        padding: 11px 12px;
        border-radius: 14px;
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 850;
        background:
            linear-gradient(90deg, rgba(37, 99, 235, 0.30), rgba(6, 182, 212, 0.12));
        border: 1px solid rgba(96, 165, 250, 0.36);
        box-shadow:
            0 14px 34px rgba(37, 99, 235, 0.18),
            inset 3px 0 0 rgba(56, 189, 248, 0.95);
    }

    .veles-nav-icon {
        color: #67E8F9;
        width: 18px;
        display: inline-flex;
        justify-content: center;
    }

    [data-testid="stSidebar"] .stButton > button {
        justify-content: flex-start;
        background: transparent;
        color: #CBD5E1;
        border: 1px solid transparent;
        border-radius: 14px;
        padding: 10px 12px;
        font-size: 14px;
        font-weight: 700;
        transition:
            background 160ms ease,
            border-color 160ms ease,
            color 160ms ease,
            transform 160ms ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(15, 23, 42, 0.72);
        border-color: rgba(148, 163, 184, 0.20);
        color: #F8FAFC;
        transform: translateX(2px);
    }

    [data-testid="stSidebar"] .stButton > button:focus,
    [data-testid="stSidebar"] .stButton > button:active {
        background: rgba(37, 99, 235, 0.16);
        border-color: rgba(96, 165, 250, 0.28);
        color: #F8FAFC;
        box-shadow: none;
    }

    .veles-sidebar-user-card {
        margin: 28px 6px 12px 6px;
        padding: 14px 14px;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.16);
    }

    .veles-user-name {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 850;
    }

    .veles-user-role {
        color: #64748B;
        font-size: 11px;
        margin-top: 4px;
    }

    
    /* Sidebar logout action */
    [data-testid="stSidebar"] .stButton:has(button[kind="secondary"]):last-of-type > button,
    [data-testid="stSidebar"] button[kind="secondary"] {
        border-radius: 14px;
    }

    [data-testid="stSidebar"] .stButton > button#sidebar_logout,
    [data-testid="stSidebar"] .stButton:has(button[title="Sign out"]) > button {
        color: #94A3B8;
    }

    [data-testid="stSidebar"] div:has(> button[kind="secondary"]) {
        margin-top: 6px;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        color: #F8FAFC;
    }

    
    /* Premium sidebar active indicator */
    .veles-nav-current {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(
                90deg,
                rgba(37,99,235,0.24),
                rgba(6,182,212,0.10)
            );
        border: 1px solid rgba(96,165,250,0.34);
        box-shadow:
            0 14px 36px rgba(37,99,235,0.20),
            inset 0 0 22px rgba(56,189,248,0.05);
    }

    .veles-nav-current::before {
        content: "";
        position: absolute;
        left: 0;
        top: 10px;
        bottom: 10px;
        width: 4px;
        border-radius: 999px;
        background: linear-gradient(
            180deg,
            #38BDF8,
            #2563EB
        );
        box-shadow:
            0 0 16px rgba(56,189,248,0.65);
    }

    .veles-nav-current .veles-nav-icon {
        color: #67E8F9;
    }

    
    /* Dashboard Research Terminal */
    .veles-terminal-hero {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 34px 36px;
        margin-bottom: 28px;
        background:
            radial-gradient(circle at 10% 0%, rgba(37,99,235,0.24), transparent 34%),
            linear-gradient(135deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 28px 72px rgba(0,0,0,0.32),
            inset 0 0 80px rgba(37,99,235,0.05);
        backdrop-filter: blur(18px);
    }

    .veles-terminal-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0.16;
        background-image:
            linear-gradient(rgba(148,163,184,0.18) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,0.18) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: radial-gradient(circle at top left, black, transparent 70%);
    }

    .veles-terminal-kicker {
        position: relative;
        color: #38BDF8;
        font-size: 12px;
        font-weight: 950;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .veles-terminal-title {
        position: relative;
        color: #F8FAFC;
        font-size: 38px;
        font-weight: 950;
        letter-spacing: -0.045em;
        margin-bottom: 8px;
    }

    .veles-terminal-subtitle {
        position: relative;
        color: #94A3B8;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 26px;
    }

    .veles-terminal-metrics {
        position: relative;
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
    }

    .veles-terminal-metric {
        padding: 16px 16px;
        border-radius: 18px;
        background: rgba(2,6,23,0.42);
        border: 1px solid rgba(148,163,184,0.16);
    }

    .veles-terminal-metric span {
        display: block;
        color: #94A3B8;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .veles-terminal-metric strong {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 950;
    }

    .veles-terminal-section-label {
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin: 6px 0 14px 2px;
    }

    .veles-command-card {
        min-height: 150px;
        padding: 22px;
        border-radius: 24px;
        background:
            linear-gradient(180deg, rgba(15,23,42,0.84), rgba(15,23,42,0.58));
        border: 1px solid rgba(148,163,184,0.18);
        box-shadow: 0 18px 42px rgba(0,0,0,0.24);
        backdrop-filter: blur(14px);
        transition: all 160ms ease;
    }

    .veles-command-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.34);
        box-shadow:
            0 24px 56px rgba(0,0,0,0.30),
            0 0 42px rgba(37,99,235,0.12);
    }

    .veles-command-icon {
        color: #38BDF8;
        font-size: 26px;
        font-weight: 950;
        margin-bottom: 18px;
    }

    .veles-command-title {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 900;
        letter-spacing: -0.025em;
        margin-bottom: 8px;
    }

    .veles-command-subtitle {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.45;
    }

    
    /* Dashboard command card routing buttons */
    .veles-command-open {
        margin-top: 18px;
        color: #38BDF8;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        margin-top: -8px;
        border-radius: 16px;
        border: 1px solid rgba(56,189,248,0.20);
        background: rgba(2,6,23,0.38);
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        transition: all 160ms ease;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button:hover {
        background: rgba(37,99,235,0.18);
        border-color: rgba(56,189,248,0.42);
        color: #F8FAFC;
        transform: translateY(-1px);
    }

    
    /* Hide dashboard command routing buttons while preserving click behavior */
    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        margin-top: -150px;
        min-height: 150px;
        height: 150px;
        opacity: 0;
        border: 0;
        background: transparent;
        cursor: pointer;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton {
        position: relative;
        z-index: 5;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.34);
        box-shadow:
            0 24px 56px rgba(0,0,0,0.30),
            0 0 42px rgba(37,99,235,0.12);
    }

    
    /* Native dashboard command card buttons */
    div[data-testid="column"] .stButton > button {
        white-space: pre-line;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button,
    div[data-testid="column"] .stButton > button:has(p) {
        min-height: 150px;
        text-align: left;
        justify-content: flex-start;
        align-items: flex-start;
        padding: 22px 24px;
        border-radius: 24px;
        background:
            linear-gradient(180deg, rgba(15,23,42,0.84), rgba(15,23,42,0.58));
        border: 1px solid rgba(148,163,184,0.18);
        box-shadow: 0 18px 42px rgba(0,0,0,0.24);
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 850;
        transition: all 160ms ease;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:hover,
    div[data-testid="column"] .stButton > button:has(p):hover {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.34);
        box-shadow:
            0 24px 56px rgba(0,0,0,0.30),
            0 0 42px rgba(37,99,235,0.12);
        background:
            linear-gradient(180deg, rgba(15,23,42,0.95), rgba(15,23,42,0.68));
        color: #F8FAFC;
    }

    
    /* Polished dashboard command launch cards */
    div[data-testid="column"] .stButton > button[kind="secondary"] {
        white-space: pre-line;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button {
        min-height: 168px;
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        text-align: left;
        padding: 26px 24px;
        border-radius: 26px;
        color: #F8FAFC;
        background:
            radial-gradient(circle at 12% 12%, rgba(56,189,248,0.16), transparent 28%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 18px 44px rgba(0,0,0,0.28),
            inset 0 0 38px rgba(37,99,235,0.04);
        font-size: 15px;
        font-weight: 850;
        line-height: 1.7;
        letter-spacing: -0.01em;
        transition: all 180ms ease;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button p {
        margin: 0;
        color: inherit;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:hover {
        transform: translateY(-3px);
        border-color: rgba(56,189,248,0.46);
        background:
            radial-gradient(circle at 12% 12%, rgba(56,189,248,0.24), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.84));
        box-shadow:
            0 26px 64px rgba(0,0,0,0.34),
            0 0 50px rgba(37,99,235,0.14);
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:active {
        transform: translateY(-1px);
    }

    
    /* Elegant command center cards */
    .veles-command-card {
        min-height: 172px;
        padding: 24px;
        border-radius: 26px;
        background:
            radial-gradient(circle at 12% 10%, rgba(56,189,248,0.18), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 20px 48px rgba(0,0,0,0.28),
            inset 0 0 42px rgba(37,99,235,0.04);
        transition: all 180ms ease;
    }

    .veles-command-topline {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    .veles-command-icon {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        color: #38BDF8;
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.18);
        font-size: 20px;
        font-weight: 950;
    }

    .veles-command-arrow {
        color: #64748B;
        font-size: 18px;
        font-weight: 900;
        transition: all 160ms ease;
    }

    .veles-command-title {
        color: #F8FAFC;
        font-size: 19px;
        font-weight: 950;
        letter-spacing: -0.035em;
        margin-bottom: 8px;
    }

    .veles-command-subtitle {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.45;
        max-width: 190px;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card {
        transform: translateY(-3px);
        border-color: rgba(56,189,248,0.42);
        box-shadow:
            0 28px 68px rgba(0,0,0,0.36),
            0 0 52px rgba(37,99,235,0.14);
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-arrow {
        color: #38BDF8;
        transform: translateX(3px);
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        margin-top: -52px;
        height: 44px;
        border-radius: 0 0 22px 22px;
        border: 1px solid rgba(56,189,248,0.16);
        border-top: 0;
        background: rgba(2,6,23,0.34);
        color: #38BDF8;
        font-size: 11px;
        font-weight: 950;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        transition: all 160ms ease;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button:hover {
        background: rgba(37,99,235,0.18);
        color: #F8FAFC;
        border-color: rgba(56,189,248,0.34);
    }

    
    /* Dashboard Sprint 2: elegant clickable command cards */
    .veles-terminal-hero {
        padding: 28px 36px !important;
        margin-bottom: 22px !important;
    }

    .veles-terminal-title {
        font-size: 34px !important;
        margin-bottom: 6px !important;
    }

    .veles-terminal-subtitle {
        margin-bottom: 0 !important;
    }

    .veles-terminal-section-label {
        margin-top: 24px !important;
        margin-bottom: 14px !important;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button {
        white-space: pre-line;
        min-height: 190px;
        width: 100%;
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        text-align: left;
        padding: 26px 28px;
        border-radius: 28px;
        color: #F8FAFC;
        background:
            radial-gradient(circle at 8% 12%, rgba(56,189,248,0.18), transparent 28%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 20px 48px rgba(0,0,0,0.28),
            inset 0 0 42px rgba(37,99,235,0.04);
        transition: all 180ms ease;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button p {
        width: 100%;
        margin: 0;
        color: inherit;
        font-size: 16px;
        font-weight: 850;
        line-height: 1.65;
        letter-spacing: -0.01em;
        text-align: left;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button:hover {
        transform: translateY(-4px);
        border-color: rgba(56,189,248,0.46);
        background:
            radial-gradient(circle at 8% 12%, rgba(56,189,248,0.26), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.86));
        box-shadow:
            0 28px 68px rgba(0,0,0,0.36),
            0 0 52px rgba(37,99,235,0.16);
        color: #F8FAFC;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button:active {
        transform: translateY(-1px);
    }

    
    /* Final dashboard command card visual override */
    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button {
        min-height: 156px !important;
        height: 156px !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        text-align: left !important;
        white-space: pre-line !important;
        padding: 28px 30px !important;
        border-radius: 26px !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 8% 10%, rgba(56,189,248,0.18), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78)) !important;
        border: 1px solid rgba(148,163,184,0.20) !important;
        box-shadow:
            0 20px 48px rgba(0,0,0,0.28),
            inset 0 0 42px rgba(37,99,235,0.04) !important;
        font-size: 15px !important;
        font-weight: 850 !important;
        line-height: 1.75 !important;
        transition: all 180ms ease !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:hover {
        transform: translateY(-3px) !important;
        border-color: rgba(56,189,248,0.46) !important;
        background:
            radial-gradient(circle at 8% 10%, rgba(56,189,248,0.26), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.86)) !important;
        color: #F8FAFC !important;
        box-shadow:
            0 28px 68px rgba(0,0,0,0.36),
            0 0 52px rgba(37,99,235,0.16) !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:focus,
    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:active {
        color: #F8FAFC !important;
        border-color: rgba(56,189,248,0.46) !important;
        background:
            radial-gradient(circle at 8% 10%, rgba(56,189,248,0.24), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.86)) !important;
        box-shadow:
            0 24px 58px rgba(0,0,0,0.32),
            0 0 42px rgba(37,99,235,0.12) !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button p {
        text-align: left !important;
        margin: 0 !important;
        color: inherit !important;
    }

    
    /* Scoped command center launch cards */
    .veles-command-center-scope + div div[data-testid="stButton"] > button,
    .veles-command-center-scope ~ div div[data-testid="stButton"] > button {
        white-space: pre-line !important;
        min-height: 178px !important;
        height: 178px !important;
        width: 100% !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 30px 32px !important;
        border-radius: 28px !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.20), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.96), rgba(2,6,23,0.82)) !important;
        border: 1px solid rgba(148,163,184,0.22) !important;
        box-shadow:
            0 22px 56px rgba(0,0,0,0.32),
            inset 0 0 42px rgba(37,99,235,0.05) !important;
        font-size: 16px !important;
        font-weight: 850 !important;
        line-height: 1.75 !important;
        letter-spacing: -0.01em !important;
        transition: all 180ms ease !important;
    }

    .veles-command-center-scope + div div[data-testid="stButton"] > button:hover,
    .veles-command-center-scope ~ div div[data-testid="stButton"] > button:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(56,189,248,0.48) !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.28), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,1), rgba(2,6,23,0.88)) !important;
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18) !important;
        color: #F8FAFC !important;
    }

    .veles-command-center-scope + div div[data-testid="stButton"] > button:focus,
    .veles-command-center-scope + div div[data-testid="stButton"] > button:active,
    .veles-command-center-scope ~ div div[data-testid="stButton"] > button:focus,
    .veles-command-center-scope ~ div div[data-testid="stButton"] > button:active {
        color: #F8FAFC !important;
        border-color: rgba(56,189,248,0.48) !important;
        box-shadow:
            0 24px 58px rgba(0,0,0,0.34),
            0 0 48px rgba(37,99,235,0.14) !important;
    }

    .veles-command-center-scope + div div[data-testid="stButton"] > button p,
    .veles-command-center-scope ~ div div[data-testid="stButton"] > button p {
        text-align: left !important;
        margin: 0 !important;
        color: inherit !important;
    }

    
    /* Restored premium HTML command cards */
    .veles-command-card {
        position: relative;
        min-height: 190px;
        padding: 26px 28px;
        border-radius: 28px;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.18), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.96), rgba(2,6,23,0.82));
        border: 1px solid rgba(148,163,184,0.22);
        box-shadow:
            0 22px 56px rgba(0,0,0,0.32),
            inset 0 0 42px rgba(37,99,235,0.05);
        transition: all 180ms ease;
        overflow: hidden;
    }

    .veles-command-card::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0;
        background:
            linear-gradient(135deg, rgba(56,189,248,0.12), transparent 38%);
        transition: opacity 180ms ease;
    }

    .veles-command-topline {
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 42px;
        z-index: 1;
    }

    .veles-command-icon {
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 15px;
        color: #38BDF8;
        background: rgba(56,189,248,0.09);
        border: 1px solid rgba(56,189,248,0.20);
        font-size: 20px;
        font-weight: 950;
        box-shadow: inset 0 0 18px rgba(56,189,248,0.08);
    }

    .veles-command-arrow {
        color: #64748B;
        font-size: 20px;
        font-weight: 950;
        transition: all 180ms ease;
    }

    .veles-command-title {
        position: relative;
        z-index: 1;
        color: #F8FAFC;
        font-size: 21px;
        font-weight: 950;
        letter-spacing: -0.04em;
        margin-bottom: 9px;
    }

    .veles-command-subtitle {
        position: relative;
        z-index: 1;
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.5;
        max-width: 260px;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card {
        transform: translateY(-4px);
        border-color: rgba(56,189,248,0.48);
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18);
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card::before {
        opacity: 1;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-arrow {
        color: #38BDF8;
        transform: translateX(4px);
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton {
        margin-top: -190px;
        height: 190px;
        position: relative;
        z-index: 10;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        height: 190px !important;
        min-height: 190px !important;
        opacity: 0 !important;
        border: 0 !important;
        background: transparent !important;
        cursor: pointer !important;
    }

    
    /* Fix dashboard card invisible routing overlay */
    div[data-testid="column"]:has(.veles-command-card) {
        position: relative;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton {
        position: relative;
        margin-top: -190px !important;
        height: 190px !important;
        z-index: 20;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        height: 190px !important;
        min-height: 190px !important;
        width: 100% !important;
        opacity: 0 !important;
        border: 0 !important;
        background: transparent !important;
        cursor: pointer !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button:hover,
    div[data-testid="column"]:has(.veles-command-card) .stButton > button:focus,
    div[data-testid="column"]:has(.veles-command-card) .stButton > button:active {
        opacity: 0 !important;
        border: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    
    /* Command cards as real links */
    .veles-command-link {
        display: block;
        text-decoration: none !important;
        color: inherit !important;
    }

    .veles-command-link:hover {
        text-decoration: none !important;
    }

    .veles-command-link .veles-command-card {
        cursor: pointer;
    }

    .veles-command-link:hover .veles-command-card {
        transform: translateY(-4px);
        border-color: rgba(56,189,248,0.48);
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18);
    }

    .veles-command-link:hover .veles-command-card::before {
        opacity: 1;
    }

    .veles-command-link:hover .veles-command-arrow {
        color: #38BDF8;
        transform: translateX(4px);
    }

    div[data-testid="column"]:has(.veles-command-link) .stButton {
        display: none !important;
    }

    
    /* Native command cards final */
    div[data-testid="column"]:has(.veles-command-button-scope) .stButton > button {
        white-space: pre-line !important;
        min-height: 190px !important;
        height: 190px !important;
        width: 100% !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 30px 32px !important;
        border-radius: 28px !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.20), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.96), rgba(2,6,23,0.82)) !important;
        border: 1px solid rgba(148,163,184,0.22) !important;
        box-shadow:
            0 22px 56px rgba(0,0,0,0.32),
            inset 0 0 42px rgba(37,99,235,0.05) !important;
        font-size: 16px !important;
        font-weight: 850 !important;
        line-height: 1.75 !important;
        letter-spacing: -0.01em !important;
        transition: all 180ms ease !important;
    }

    div[data-testid="column"]:has(.veles-command-button-scope) .stButton > button:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(56,189,248,0.48) !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.28), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,1), rgba(2,6,23,0.88)) !important;
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18) !important;
        color: #F8FAFC !important;
    }

    div[data-testid="column"]:has(.veles-command-button-scope) .stButton > button:focus,
    div[data-testid="column"]:has(.veles-command-button-scope) .stButton > button:active {
        color: #F8FAFC !important;
        border-color: rgba(56,189,248,0.48) !important;
        box-shadow:
            0 24px 58px rgba(0,0,0,0.34),
            0 0 48px rgba(37,99,235,0.14) !important;
    }

    div[data-testid="column"]:has(.veles-command-button-scope) .stButton > button p {
        text-align: left !important;
        margin: 0 !important;
        color: inherit !important;
    }

    
    /* Final native dashboard command cards */
    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button {
        white-space: pre-line !important;
        min-height: 190px !important;
        height: 190px !important;
        width: 100% !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 28px 30px !important;
        border-radius: 28px !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.20), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.96), rgba(2,6,23,0.82)) !important;
        border: 1px solid rgba(148,163,184,0.22) !important;
        box-shadow:
            0 22px 56px rgba(0,0,0,0.32),
            inset 0 0 42px rgba(37,99,235,0.05) !important;
        transition: all 180ms ease !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button p {
        margin: 0 !important;
        text-align: left !important;
        color: inherit !important;
        font-size: 16px !important;
        font-weight: 850 !important;
        line-height: 1.75 !important;
        letter-spacing: -0.01em !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(56,189,248,0.48) !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.28), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,1), rgba(2,6,23,0.88)) !important;
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18) !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button:focus,
    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button:active {
        color: #F8FAFC !important;
        border-color: rgba(56,189,248,0.48) !important;
        box-shadow:
            0 24px 58px rgba(0,0,0,0.34),
            0 0 48px rgba(37,99,235,0.14) !important;
    }

    
    /* Research Intelligence panel */
    .veles-mini-panel-title {
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 2px 0 14px 2px;
    }

    
    /* Dashboard spacing polish */
    .veles-terminal-section-label {
        margin-top: 18px !important;
        margin-bottom: 12px !important;
    }

    .veles-terminal-metric {
        margin-bottom: 6px;
    }

    
    /* Research Workspace company terminal hero */
    .veles-company-terminal-hero {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 34px 38px;
        margin-bottom: 26px;
        background:
            radial-gradient(circle at 12% 0%, rgba(56,189,248,0.22), transparent 32%),
            linear-gradient(135deg, rgba(15,23,42,0.95), rgba(2,6,23,0.80));
        border: 1px solid rgba(148,163,184,0.22);
        box-shadow:
            0 28px 72px rgba(0,0,0,0.34),
            inset 0 0 72px rgba(37,99,235,0.05);
        backdrop-filter: blur(18px);
    }

    .veles-company-terminal-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0.14;
        background-image:
            linear-gradient(rgba(148,163,184,0.18) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,0.18) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: radial-gradient(circle at top left, black, transparent 72%);
    }

    .veles-company-terminal-kicker {
        position: relative;
        color: #38BDF8;
        font-size: 12px;
        font-weight: 950;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .veles-company-terminal-title {
        position: relative;
        color: #F8FAFC;
        font-size: 44px;
        font-weight: 950;
        letter-spacing: -0.055em;
        margin-bottom: 8px;
    }

    .veles-company-terminal-subtitle {
        position: relative;
        color: #CBD5E1;
        font-size: 15px;
        font-weight: 750;
        margin-bottom: 14px;
    }

    .veles-company-terminal-description {
        position: relative;
        color: #94A3B8;
        font-size: 14px;
        line-height: 1.6;
        max-width: 760px;
    }

    
    /* DCF workflow spacing fix */
    .veles-sticky-workflow {
        padding: 0 !important;
        margin: 0 0 22px 0 !important;
        min-height: auto !important;
        height: auto !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }

    
    /* Compact DCF workflow */
    .veles-workflow-shell {
        padding: 16px 20px !important;
        border-radius: 18px !important;
        margin-bottom: 14px !important;
    }

    .veles-workflow-card {
        min-height: 88px !important;
        height: 88px !important;
        padding: 16px 18px !important;
        border-radius: 18px !important;
    }

    .veles-workflow-status {
        font-size: 13px !important;
        margin-bottom: 12px !important;
    }

    .veles-workflow-title {
        font-size: 13px !important;
        font-weight: 900 !important;
        letter-spacing: -0.01em !important;
    }

    .veles-step-breadcrumb {
        margin: 16px 0 22px 0;
        padding: 14px 18px;
        border-radius: 16px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(15,23,42,0.58);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .veles-step-breadcrumb span {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 800;
    }

    .veles-step-breadcrumb strong {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 950;
        letter-spacing: -0.02em;
    }

    </style>
    """, unsafe_allow_html=True)


def page_header(title, subtitle):
    st.markdown(f"""
    <div class="veles-page-title">{title}</div>
    <div class="veles-page-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)


def metric_card(label, value, change=None, positive=True):
    change_class = "veles-metric-change-positive" if positive else "veles-metric-change-negative"
    change_html = f'<div class="{change_class}">{change}</div>' if change else ""

    st.markdown(f"""
    <div class="veles-card">
        <div class="veles-metric-label">{label}</div>
        <div class="veles-metric-value">{value}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)


def insight_card(title, text):
    st.markdown(f"""
    <div class="veles-card">
        <div class="veles-insight-title">{title}</div>
        <div class="veles-insight-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def company_card(name, stage, valuation, sector="Brain-Computer Interface", funding=None):
    if funding:
        body = f"""
        <div class="veles-card">
            <div class="veles-company-name">{name}</div>
            <div class="veles-company-meta">{sector}</div>
            <div class="veles-company-meta">{stage}</div>
            <div class="veles-company-meta">Funding: {funding}</div>
            <div class="veles-company-meta">Valuation: {valuation}</div>
            <div class="veles-button-link">Open →</div>
        </div>
        """
    else:
        body = f"""
        <div class="veles-card">
            <div class="veles-company-name">{name}</div>
            <div class="veles-company-meta">{sector}</div>
            <div class="veles-company-meta">{stage}</div>
            <div class="veles-company-meta">Valuation: {valuation}</div>
            <div class="veles-button-link">Open →</div>
        </div>
        """

    st.markdown(body, unsafe_allow_html=True)

def section_title(title, subtitle=None):
    subtitle_html = f'<div class="veles-page-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div style="margin-top: 18px; margin-bottom: 12px;">
        <div style="font-size: 22px; font-weight: 800; color: #F8FAFC;">{title}</div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def activity_item(title, description, meta=""):
    meta_html = f'<div class="veles-company-meta">{meta}</div>' if meta else ""
    st.markdown(f"""
    <div class="veles-card">
        <div class="veles-company-name" style="font-size: 17px;">{title}</div>
        <div class="veles-insight-text" style="font-size: 14px;">{description}</div>
        {meta_html}
    </div>
    """, unsafe_allow_html=True)


def status_pill(label, status="Neutral"):
    color = {
        "Positive": "#10B981",
        "Warning": "#F59E0B",
        "Danger": "#EF4444",
        "Neutral": "#3B82F6",
    }.get(status, "#3B82F6")

    st.markdown(f"""
    <span style="
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.12);
        color: {color};
        border: 1px solid #1E293B;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.02em;
    ">
        {label}
    </span>
    """, unsafe_allow_html=True)


def ai_workflow_card(title, steps):
    st.markdown(f"""
    <div class="veles-card">
        <div class="veles-insight-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

    for step in steps:
        st.markdown(f"✓ {step}")
