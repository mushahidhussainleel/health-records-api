from fastapi import FastAPI
from app.routers import auth, health_records , medicine_records
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Health Records Storage API",
   description="This project addresses a critical healthcare problem: the loss and unavailability of patient medical records. When patients move between hospitals, their reports, prescriptions, and medical history are often missing, which can be dangerous in emergency situations.",
    version="0.1.0"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        description=app.description,
        version=app.version,
        routes=app.routes
    )

    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token (Swagger will automatically add 'Bearer' prefix)"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(health_records.router , prefix="/health-records", tags=["Health Records"])
app.include_router(medicine_records.router,prefix="/medicines-records",tags=["Medicines"])

@app.get("/", response_class=HTMLResponse , tags=["Root"])
def read_root():
    """
    Simple HTML welcome page with links to Swagger and ReDoc docs.
    """

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Records Storage API - Welcome</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            overflow-x: hidden;
        }

        /* Animated Gradient Background */
        .bg-gradient {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, #0f172a, #1e293b, #334155, #1e40af);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            z-index: 0;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Advanced Particle System */
        .particles-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 1;
            pointer-events: none;
        }

        .particle {
            position: absolute;
            background: rgba(96, 165, 250, 0.4);
            border-radius: 50%;
            box-shadow: 0 0 20px rgba(96, 165, 250, 0.6);
        }

        .particle:nth-child(1) { width: 4px; height: 4px; top: 20%; left: 10%; animation: float1 15s infinite; }
        .particle:nth-child(2) { width: 6px; height: 6px; top: 60%; left: 80%; animation: float2 18s infinite; }
        .particle:nth-child(3) { width: 3px; height: 3px; top: 40%; left: 30%; animation: float3 20s infinite; }
        .particle:nth-child(4) { width: 5px; height: 5px; top: 70%; left: 50%; animation: float1 17s infinite; }
        .particle:nth-child(5) { width: 4px; height: 4px; top: 30%; left: 90%; animation: float2 16s infinite; }
        .particle:nth-child(6) { width: 6px; height: 6px; top: 80%; left: 20%; animation: float3 19s infinite; }
        .particle:nth-child(7) { width: 3px; height: 3px; top: 50%; left: 70%; animation: float1 21s infinite; }
        .particle:nth-child(8) { width: 5px; height: 5px; top: 15%; left: 60%; animation: float2 14s infinite; }

        @keyframes float1 {
            0%, 100% { transform: translate(0, 0) rotate(0deg); opacity: 0.3; }
            25% { transform: translate(100px, -100px) rotate(90deg); opacity: 0.7; }
            50% { transform: translate(200px, 0px) rotate(180deg); opacity: 0.5; }
            75% { transform: translate(100px, 100px) rotate(270deg); opacity: 0.8; }
        }

        @keyframes float2 {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.4; }
            33% { transform: translate(-120px, 80px) scale(1.5); opacity: 0.8; }
            66% { transform: translate(80px, -120px) scale(0.8); opacity: 0.6; }
        }

        @keyframes float3 {
            0%, 100% { transform: translate(0, 0) rotate(0deg) scale(1); opacity: 0.3; }
            50% { transform: translate(-100px, -100px) rotate(180deg) scale(1.3); opacity: 0.9; }
        }

        /* Grid Pattern Overlay */
        .grid-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(96, 165, 250, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(96, 165, 250, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            z-index: 1;
            pointer-events: none;
        }

        .main-wrapper {
            position: relative;
            z-index: 2;
            padding: 40px 20px;
            max-width: 1400px;
            margin: 0 auto;
        }

        /* Glassmorphism Header */
        .header {
            text-align: center;
            margin-bottom: 40px;
            animation: fadeInDown 1s ease-out;
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .logo-container {
            position: relative;
            display: inline-block;
            margin-bottom: 20px;
        }

        .logo {
            font-size: 80px;
            filter: drop-shadow(0 0 30px rgba(96, 165, 250, 0.8));
            animation: logoFloat 3s ease-in-out infinite;
        }

        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-15px) rotate(5deg); }
        }

        .glow-ring {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 160px;
            height: 160px;
            border: 3px solid rgba(96, 165, 250, 0.3);
            border-radius: 50%;
            animation: ringPulse 2s ease-in-out infinite;
        }

        @keyframes ringPulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.5; }
        }

        .header h1 {
            font-size: 2.8em;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }

        .header .subtitle {
            font-size: 1.2em;
            color: #94a3b8;
            margin-bottom: 20px;
        }

        .status-bar {
            display: inline-flex;
            align-items: center;
            gap: 20px;
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(20px);
            padding: 12px 30px;
            border-radius: 50px;
            border: 1px solid rgba(96, 165, 250, 0.2);
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95em;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10b981;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.2); }
        }

        /* Main Content Grid */
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 30px;
        }

        /* Glass Card */
        .glass-card {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(96, 165, 250, 0.2);
            padding: 25px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.8s ease-out backwards;
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.1), transparent);
            transition: left 0.7s;
        }

        .glass-card:hover::before {
            left: 100%;
        }

        .glass-card:hover {
            transform: translateY(-8px);
            border-color: rgba(96, 165, 250, 0.5);
            box-shadow: 0 20px 60px rgba(96, 165, 250, 0.3);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }

        .card-icon {
            font-size: 2em;
            filter: drop-shadow(0 0 10px currentColor);
        }

        .card-title {
            font-size: 1.4em;
            font-weight: 700;
            color: #e2e8f0;
        }

        /* Endpoints Section */
        .endpoints-section {
            grid-column: 1 / -1;
        }

        .endpoint-categories {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .endpoint-category {
            background: rgba(15, 23, 42, 0.6);
            border-radius: 14px;
            padding: 20px;
            border: 1px solid rgba(96, 165, 250, 0.15);
        }

        .category-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(96, 165, 250, 0.2);
        }

        .category-icon {
            font-size: 1.8em;
        }

        .category-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #60a5fa;
        }

        .endpoint {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            margin-bottom: 10px;
            background: rgba(30, 41, 59, 0.4);
            border-radius: 10px;
            border-left: 3px solid transparent;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .endpoint:hover {
            background: rgba(30, 41, 59, 0.8);
            transform: translateX(8px);
            border-left-color: currentColor;
        }

        .method {
            font-weight: 700;
            font-size: 0.8em;
            padding: 4px 10px;
            border-radius: 6px;
            min-width: 60px;
            text-align: center;
            letter-spacing: 0.5px;
        }

        .method-post { background: #10b981; color: white; }
        .method-get { background: #3b82f6; color: white; }
        .method-put { background: #f59e0b; color: white; }
        .method-delete { background: #ef4444; color: white; }

        .endpoint-path {
            flex: 1;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            color: #94a3b8;
        }

        .endpoint-desc {
            font-size: 0.85em;
            color: #64748b;
        }

        /* Features Grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }

        .feature-item {
            padding: 25px;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 16px;
            border: 1px solid rgba(96, 165, 250, 0.15);
            transition: all 0.4s ease;
        }

        .feature-item:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(96, 165, 250, 0.4);
            transform: translateY(-5px);
        }

        .feature-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            display: inline-block;
            filter: drop-shadow(0 0 10px currentColor);
        }

        .feature-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 10px;
            color: #e2e8f0;
        }

        .feature-desc {
            color: #94a3b8;
            line-height: 1.6;
            font-size: 0.95em;
        }

        /* CTA Buttons */
        .cta-section {
            text-align: center;
            margin-top: 30px;
            animation: fadeInUp 1.2s ease-out backwards;
        }

        .cta-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }

        .cta-button {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 18px 40px;
            font-size: 1.1em;
            font-weight: 600;
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .cta-primary {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
        }

        .cta-primary::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .cta-primary:hover::before {
            width: 400px;
            height: 400px;
        }

        .cta-primary:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 50px rgba(59, 130, 246, 0.6);
        }

        .cta-secondary {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(20px);
            color: #60a5fa;
            border: 2px solid rgba(96, 165, 250, 0.3);
        }

        .cta-secondary:hover {
            background: rgba(30, 41, 59, 0.9);
            border-color: rgba(96, 165, 250, 0.6);
            transform: translateY(-5px);
        }

        .button-icon {
            font-size: 1.2em;
            position: relative;
            z-index: 1;
        }

        .button-text {
            position: relative;
            z-index: 1;
        }

        /* Stats Section */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }

        .stat-card {
            text-align: center;
            padding: 25px;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 16px;
            border: 1px solid rgba(96, 165, 250, 0.15);
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            color: #94a3b8;
            margin-top: 8px;
            font-size: 0.95em;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 30px 20px;
            margin-top: 40px;
            border-top: 1px solid rgba(96, 165, 250, 0.1);
            color: #64748b;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .footer-link {
            color: #60a5fa;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .footer-link:hover {
            color: #3b82f6;
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            .endpoint-categories {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.5em;
            }

            .logo {
                font-size: 70px;
            }

            .cta-buttons {
                flex-direction: column;
            }

            .stats-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        /* Animation Delays */
        .glass-card:nth-child(1) { animation-delay: 0.1s; }
        .glass-card:nth-child(2) { animation-delay: 0.2s; }
        .glass-card:nth-child(3) { animation-delay: 0.3s; }
        .glass-card:nth-child(4) { animation-delay: 0.4s; }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="grid-overlay"></div>
    
    <!-- Particle System -->
    <div class="particles-container">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>

    <div class="main-wrapper">
        <!-- Header -->
        <div class="header">
            <div class="logo-container">
                <div class="glow-ring"></div>
                <div class="logo">🏥</div>
            </div>
            <h1>Health Records Storage API</h1>
            <p class="subtitle">Enterprise-Grade Healthcare Data Management</p>
            <div class="status-bar">
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>API Live</span>
                </div>
                <div class="status-item">
                    <span>📡</span>
                    <span>v0.1.0</span>
                </div>
                <div class="status-item">
                    <span>⚡</span>
                    <span>FastAPI</span>
                </div>
            </div>
        </div>

        <!-- Content Grid -->
        <div class="content-grid">
            <!-- Mission Card -->
            <div class="glass-card">
                <div class="card-header">
                    <div class="card-icon">🎯</div>
                    <h2 class="card-title">Our Mission</h2>
                </div>
                <p style="color: #94a3b8; line-height: 1.8; font-size: 1.05em;">
                    Solving a critical healthcare challenge: the loss of patient medical records. When patients move between hospitals, their vital health data often goes missing—potentially life-threatening in emergencies. We provide a secure, centralized solution accessible anywhere, anytime.
                </p>
            </div>

            <!-- Stats Card -->
            <div class="glass-card">
                <div class="card-header">
                    <div class="card-icon">📊</div>
                    <h2 class="card-title">API Statistics</h2>
                </div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">13</div>
                        <div class="stat-label">Endpoints</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">3</div>
                        <div class="stat-label">Modules</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">100%</div>
                        <div class="stat-label">Secure</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">24/7</div>
                        <div class="stat-label">Available</div>
                    </div>
                </div>
            </div>

            <!-- API Endpoints -->
            <div class="glass-card endpoints-section">
                <div class="card-header">
                    <div class="card-icon">🔗</div>
                    <h2 class="card-title">API Endpoints</h2>
                </div>
                <div class="endpoint-categories">
                    <div class="endpoint-category">
                        <div class="category-header">
                            <span class="category-icon">🔐</span>
                            <h3 class="category-title">Authentication</h3>
                        </div>
                        <div class="endpoint">
                            <span class="method method-post">POST</span>
                            <span class="endpoint-path">/auth/signup</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-post">POST</span>
                            <span class="endpoint-path">/auth/login</span>
                        </div>
                    </div>

                    <div class="endpoint-category">
                        <div class="category-header">
                            <span class="category-icon">🏥</span>
                            <h3 class="category-title">Health Records</h3>
                        </div>
                        <div class="endpoint">
                            <span class="method method-post">POST</span>
                            <span class="endpoint-path">/health-records/</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-get">GET</span>
                            <span class="endpoint-path">/health-records/</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-get">GET</span>
                            <span class="endpoint-path">/health-records/{id}</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-put">PUT</span>
                            <span class="endpoint-path">/health-records/{id}</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-delete">DELETE</span>
                            <span class="endpoint-path">/health-records/{id}</span>
                        </div>
                    </div>

                    <div class="endpoint-category">
                        <div class="category-header">
                            <span class="category-icon">💊</span>
                            <h3 class="category-title">Medicines</h3>
                        </div>
                        <div class="endpoint">
                            <span class="method method-post">POST</span>
                            <span class="endpoint-path">/medicines-records/</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-get">GET</span>
                            <span class="endpoint-path">/medicines-records/</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-get">GET</span>
                            <span class="endpoint-path">/medicines-records/{id}</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-put">PUT</span>
                            <span class="endpoint-path">/medicines-records/{id}</span>
                        </div>
                        <div class="endpoint">
                            <span class="method method-delete">DELETE</span>
                            <span class="endpoint-path">/medicines-records/{id}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features -->
            <div class="glass-card" style="grid-column: 1 / -1;">
                <div class="card-header">
                    <div class="card-icon">✨</div>
                    <h2 class="card-title">Powerful Features</h2>
                </div>
                <div class="features-grid">
                    <div class="feature-item">
                        <div class="feature-icon">🔒</div>
                        <div class="feature-title">JWT Authentication</div>
                        <p class="feature-desc">Military-grade security with JSON Web Tokens protecting every request</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">📄</div>
                        <div class="feature-title">File Management</div>
                        <p class="feature-desc">Upload PDFs, X-rays, reports with automatic version control</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">💊</div>
                        <div class="feature-title">Medicine Tracking</div>
                        <p class="feature-desc">Complete prescription management with dosage and side effects</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">⚡</div>
                        <div class="feature-title">Lightning Fast</div>
                        <p class="feature-desc">Built on FastAPI for incredible performance and async support</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🌍</div>
                        <div class="feature-title">Always Accessible</div>
                        <p class="feature-desc">Cloud-based solution accessible from anywhere, 24/7</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🛡️</div>
                        <div class="feature-title">Data Isolation</div>
                        <p class="feature-desc">Complete user data separation with row-level security</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- CTA Section -->
        <div class="cta-section">
            <h2 style="font-size: 2.5em; margin-bottom: 15px; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                Start Exploring Now
            </h2>
            <p style="color: #94a3b8; font-size: 1.2em; margin-bottom: 20px;">
                Interactive documentation with live testing capabilities
            </p>
            <div class="cta-buttons">
                <a href="/docs" class="cta-button cta-primary">
                    <span class="button-icon">📖</span>
                    <span class="button-text">Swagger UI</span>
                </a>
                <a href="/redoc" class="cta-button cta-secondary">
                    <span class="button-icon">📘</span>
                    <span class="button-text">ReDoc</span>
                </a>
                <a href="/openapi.json" class="cta-button cta-secondary">
                    <span class="button-icon">📋</span>
                    <span class="button-text">OpenAPI Spec</span>
                </a>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p style="font-size: 1.1em; margin-bottom: 10px;">
                Built with ❤️ using <strong style="color: #60a5fa;">FastAPI</strong>
            </p>
            <p>Securing Healthcare Data, One Record at a Time</p>
            <div class="footer-links">
                <a href="http://127.0.0.1:8002/docs" class="footer-link">Documentation</a>
                <a href="http://127.0.0.1:8002/redoc" class="footer-link">API Reference</a>
                <a href="http://127.0.0.1:8002/openapi.json" class="footer-link">OpenAPI JSON</a>
            </div>
            <p style="margin-top: 20px; font-size: 0.9em;">
                Running on <code style="color: #60a5fa; background: rgba(96, 165, 250, 0.1); padding: 2px 8px; border-radius: 4px;">http://127.0.0.1:8002</code>
            </p>
        </div>
    </div>

    <script>
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });

        // Intersection Observer for animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Animate endpoints on scroll
        document.querySelectorAll('.endpoint').forEach((endpoint, index) => {
            endpoint.style.opacity = '0';
            endpoint.style.transform = 'translateX(-20px)';
            endpoint.style.transition = `all 0.5s ease ${index * 0.05}s`;
            
            setTimeout(() => {
                endpoint.style.opacity = '1';
                endpoint.style.transform = 'translateX(0)';
            }, 300);
        });

        // Animate feature items
        document.querySelectorAll('.feature-item').forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(30px)';
            item.style.transition = `all 0.6s ease ${index * 0.1}s`;
            
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, 400);
        });

        // Add hover effect to cards
        document.querySelectorAll('.glass-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });
    </script>
</body>
</html>
"""

    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
    # uvicorn main:app --reload
