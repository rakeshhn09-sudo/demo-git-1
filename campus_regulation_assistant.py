import os
import gradio as gr

gr.close_all()  # Close active servers

APP_TITLE = "🎓 NEXUS: Elite Student Academic Portal"
APP_DESCRIPTION = "Welcome to the next-generation academic portal. Access authenticated credentials, track overall transcript metrics, and consult with our hyper-accurate, 10-domain trained RAG engine for real-time compliance information."

USER_CREDENTIALS = {
    "alex": os.environ.get("NEXUS_ALEX_PASSWORD", ""),
    "taylor": os.environ.get("NEXUS_TAYLOR_PASSWORD", "")
}

STUDENT_DATA = {
    "name": "Sample Student",
    "id": "DEMO-0001",
    "major": "Computer Science",
    "semester": "Sample Term",
    "cgpa": "3.50",
    "overall_percentage": "85%",
    "overall_attendance": "90%",
    "overall_status": "SAMPLE",
    "backlog_details": "Sample data only",
    "advisor": "Sample Advisor",
    "department": "Sample Department",
    "subjects": [
        {
            "code": "CS-101",
            "name": "Sample Programming Course",
            "attendance_pct": 90,
            "internals": "25 / 30",
            "externals": "60 / 70",
            "total": 85,
            "status": "PASS"
        },
        {
            "code": "MATH-101",
            "name": "Sample Mathematics Course",
            "attendance_pct": 90,
            "internals": "25 / 30",
            "externals": "60 / 70",
            "total": 85,
            "status": "PASS"
        },
        {
            "code": "SCI-101",
            "name": "Sample Science Course",
            "attendance_pct": 90,
            "internals": "25 / 30",
            "externals": "60 / 70",
            "total": 85,
            "status": "PASS"
        },
        {
            "code": "ENG-101",
            "name": "Sample Writing Course",
            "attendance_pct": 90,
            "internals": "25 / 30",
            "externals": "60 / 70",
            "total": 85,
            "status": "PASS"
        }
    ]
}

def authenticate_student(username, password):
    username_clean = username.strip().lower()
    if username_clean in USER_CREDENTIALS and USER_CREDENTIALS[username_clean] == password:
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            ""
        )
    else:
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            "❌ Authentication failed. Check the configured credentials."
        )

def on_upload(file):
    if file is None:
        return "No file uploaded."
    try:
        return build_knowledge_base(read_pdf(file), os.path.basename(file))
    except Exception as e:
        raise gr.Error(f"The PDF could not be read: {e}")

def on_ask(question):
    if not question.strip():
        raise gr.Error("Please ask a valid question.")
    reply, found = answer(question)
    sources = ""
    for i, c in enumerate(found, start=1):
        sources += f"<div class='citation-box'><strong>Passage {i} (Page {c['page']} | Match Score: {c['score']:.2f})</strong><br><p>{c['text']}</p></div>"
    return reply, sources

def render_academic_portal():
    rows_html = ""
    for sub in STUDENT_DATA["subjects"]:
        att_color = "#10b981" if sub["attendance_pct"] >= 90 else "#f59e0b"
        status_badge = "<span style='background-color: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: bold;'>PASS</span>"

        rows_html += f"""
        <tr style='border-bottom: 1px solid #f1f5f9; transition: background-color 0.2s ease;'>
            <td style='padding: 16px 12px; font-weight: 700; color: #1e293b;'>{sub['code']}</td>
            <td style='padding: 16px 12px; color: #334155; font-weight: 500;'>{sub['name']}</td>
            <td style='padding: 16px 12px;'>
                <div style='display: flex; align-items: center; gap: 8px;'>
                    <div style='background-color: #e2e8f0; width: 60px; height: 6px; border-radius: 9999px; overflow: hidden;'>
                        <div style='background-color: {att_color}; width: {sub['attendance_pct']}%; height: 100%;'></div>
                    </div>
                    <span style='font-size: 0.85rem; font-weight: 700; color: #1e293b;'>{sub['attendance_pct']}%</span>
                </div>
            </td>
            <td style='padding: 16px 12px; text-align: center; color: #475569;'>{sub['internals']}</td>
            <td style='padding: 16px 12px; text-align: center; color: #475569;'>{sub['externals']}</td>
            <td style='padding: 16px 12px; text-align: center; font-weight: 700; color: #0f172a;'>{sub['total']} / 100</td>
            <td style='padding: 16px 12px; text-align: center;'>{status_badge}</td>
        </tr>
        """

    dashboard_html = f"""
    <div style='background-color: #ffffff; border-radius: 16px; font-family: system-ui, -apple-system, sans-serif;'>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 30px;'>
            <div style='background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; padding: 20px; border-radius: 14px; position: relative; overflow: hidden;'>
                <div style='position: absolute; right: -15px; bottom: -15px; font-size: 80px; opacity: 0.1; font-weight: 900; color: #1e3a8a;'>GPA</div>
                <span style='color: #1e40af; font-size: 0.8rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em;'>Academic Standing</span>
                <div style='font-size: 2rem; font-weight: 800; color: #1e3a8a; margin-top: 6px;'>{STUDENT_DATA['cgpa']} CGPA</div>
                <span style='color: #2563eb; font-size: 0.9rem; font-weight: 600;'>Overall Score: {STUDENT_DATA['overall_percentage']}</span>
            </div>
            <div style='background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 1px solid #a7f3d0; padding: 20px; border-radius: 14px; position: relative; overflow: hidden;'>
                <div style='position: absolute; right: -15px; bottom: -15px; font-size: 80px; opacity: 0.1; font-weight: 900; color: #065f46;'>ATT</div>
                <span style='color: #065f46; font-size: 0.8rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em;'>Presence Rating</span>
                <div style='font-size: 2rem; font-weight: 800; color: #065f46; margin-top: 6px;'>{STUDENT_DATA['overall_attendance']}</div>
                <span style='color: #059669; font-size: 0.9rem; font-weight: 600;'>Status: Satisfactory</span>
            </div>
            <div style='background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border: 1px solid #e9d5ff; padding: 20px; border-radius: 14px; position: relative; overflow: hidden;'>
                <div style='position: absolute; right: -15px; bottom: -15px; font-size: 80px; opacity: 0.1; font-weight: 900; color: #581c87;'>REG</div>
                <span style='color: #581c87; font-size: 0.8rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em;'>Pending Backlogs</span>
                <div style='font-size: 2rem; font-weight: 800; color: #581c87; margin-top: 6px;'>{STUDENT_DATA['backlog_details']}</div>
                <span style='color: #7c3aed; font-size: 0.9rem; font-weight: 600;'>Good Academic Standing</span>
            </div>
        </div>
        <div style='border-bottom: 2px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;'>
            <h3 style='color: #0f172a; margin: 0; font-size: 1.4rem; font-weight: 800;'>📋 Certified Academic Transcript</h3>
            <span style='font-size: 0.85rem; background-color: #f1f5f9; padding: 6px 12px; border-radius: 6px; font-weight: 600; color: #475569;'>Term: {STUDENT_DATA['semester']}</span>
        </div>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; background-color: #f8fafc; padding: 16px; border-radius: 10px; border: 1px solid #e2e8f0;'>
            <div><strong style='color: #64748b; font-size: 0.8rem; text-transform: uppercase;'>Institution</strong><br><span style='font-weight: 600; color: #334155; font-size: 0.95rem;'>{STUDENT_DATA['department']}</span></div>
            <div><strong style='color: #64748b; font-size: 0.8rem; text-transform: uppercase;'>Assigned Advisor</strong><br><span style='font-weight: 600; color: #334155; font-size: 0.95rem;'>{STUDENT_DATA['advisor']}</span></div>
            <div><strong style='color: #64748b; font-size: 0.8rem; text-transform: uppercase;'>Current Program</strong><br><span style='font-weight: 600; color: #334155; font-size: 0.95rem;'>{STUDENT_DATA['major']} Degree</span></div>
        </div>
        <div style='overflow-x: auto; border-radius: 12px; border: 1px solid #f0f3f6;'>
            <table style='width: 100%; border-collapse: collapse; text-align: left; min-width: 700px;'>
                <thead>
                    <tr style='background-color: #f8fafc; border-bottom: 2px solid #e2e8f0;'>
                        <th style='padding: 14px 12px; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;'>Code</th>
                        <th style='padding: 14px 12px; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;'>Subject Title</th>
                        <th style='padding: 14px 12px; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;'>Attendance Tracker</th>
                        <th style='padding: 14px 12px; text-align: center; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;'>Internals (30)</th>
                        <th style='padding: 14px 12px; text-align: center; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;'>Semester End (70)</th>
                        <th style='padding: 14px 12px; text-align: center; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;'>Total (100)</th>
                        <th style='padding: 14px 12px; text-align: center; color: #475569; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;'>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </div>
    """
    return dashboard_html

custom_css = """
.gradio-container {
    max-width: 1280px !important;
    margin: auto !important;
    padding: 40px 20px !important;
    background-color: #f6f8fc !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}
.beauty-card {
    border: 1px solid #eef2f6 !important;
    border-radius: 20px !important;
    padding: 30px !important;
    background: #ffffff !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.02), 0 8px 10px -6px rgba(0, 0, 0, 0.02) !important;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s ease !important;
}
.beauty-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 20px 35px -5px rgba(37, 99, 235, 0.08), 0 10px 15px -5px rgba(37, 99, 235, 0.03) !important;
    border-color: #2563eb !important;
}
.login-card {
    max-width: 480px;
    margin: 60px auto !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 24px !important;
    padding: 40px !important;
    background: #ffffff !important;
    box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.header-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%) !important;
    padding: 40px !important;
    border-radius: 24px !important;
    color: #ffffff !important;
    margin-bottom: 30px !important;
    box-shadow: 0 20px 40px -10px rgba(30, 58, 138, 0.3) !important;
}
.header-box h1 {
    color: #ffffff !important;
    font-size: 2.5rem !important;
    font-weight: 900 !important;
    margin-bottom: 10px !important;
}
.header-box p {
    color: #cbd5e1 !important;
    font-size: 1.15rem !important;
    line-height: 1.6 !important;
}
.header-kb-source {
    text-align: right !important;
    color: #ffffff !important;
}
.header-kb-source p, .header-kb-source span, .header-kb-source div {
    color: #ffffff !important;
}
.answer-card {
    border: 1px solid #dbeafe !important;
    border-left: 6px solid #2563eb !important;
    background: #f8fafc !important;
    border-radius: 12px !important;
    padding: 24px !important;
}
.citation-box {
    background-color: #fafbfd;
    border: 1px solid #e4ecf3;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
}
button {
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease-in-out !important;
}
button.primary {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: white !important;
}
button.primary:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3) !important;
}
input, textarea {
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
input:focus, textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
}
"""

with gr.Blocks(title="NEXUS Portal") as demo:

    # ================= LOGIN INTERFACE =================
    with gr.Column(elem_classes="login-card", visible=True) as login_container:
        gr.HTML("""
        <div style='text-align: center; margin-bottom: 24px;'>
            <div style='font-size: 40px; margin-bottom: 10px;'>🎓</div>
            <h2 style='font-size: 1.8rem; font-weight: 800; color: #0f172a; margin: 0;'>NEXUS STUDENT PORTAL</h2>
            <p style='color: #64748b; font-size: 0.95rem; margin-top: 6px;'>Please authenticate using your credentials to enter the workspace.</p>
        </div>
        """)

        username_input = gr.Textbox(label="Username / Student ID", placeholder="e.g., alex", max_lines=1)
        password_input = gr.Textbox(label="Password", placeholder="••••••••", type="password", max_lines=1)
        login_btn = gr.Button("Secure Sign In", variant="primary")
        login_error = gr.Markdown(value="", elem_id="login-error")

        gr.HTML("""
        <div style='margin-top: 20px; padding: 12px; background-color: #f8fafc; border-radius: 8px; border: 1px dashed #cbd5e1; text-align: center;'>
            <span style='font-size: 0.8rem; color: #64748b;'>Configure <code>NEXUS_ALEX_PASSWORD</code> or <code>NEXUS_TAYLOR_PASSWORD</code> in the environment before signing in.</span>
        </div>
        """)

    # ================= SECURED MAIN WEBSITE INTERFACE =================
    with gr.Column(visible=False) as main_portal_container:

        # Beautiful premium layout header
        with gr.Row(elem_classes="header-box"):
            with gr.Column(scale=4):
                gr.Markdown(f"# {APP_TITLE}")
                gr.Markdown(f"{APP_DESCRIPTION}")
            with gr.Column(scale=1, min_width=180, elem_classes="header-kb-source"):
                status_md = gr.Markdown(f"📜 **Knowledge Base Source:**\n`{knowledge_base['name'] or 'None'}`")

        with gr.Tabs():

            # TAB 1: ACADEMIC TRANSCRIPT & METRICS
            with gr.TabItem("🎓 Academic Hub", id="performance_tab"):
                with gr.Column(elem_classes="beauty-card"):
                    gr.HTML(value=render_academic_portal())

            # TAB 2: SMART DOCUMENT CONSULTANT & AI RAG CHAT
            with gr.TabItem("💬 AI Document Assistant (RAG)", id="rag_tab"):
                with gr.Row(equal_height=True):
                    with gr.Column(scale=1, elem_classes="beauty-card"):
                        gr.Markdown("### 📁 1. Document Management")
                        pdf_input = gr.File(label="Upload Academic PDF", file_types=[".pdf"], type="filepath")
                        sample_btn = gr.Button("💡 Auto-Load Integrated Academic Database", variant="secondary")

                    with gr.Column(scale=2, elem_classes="beauty-card"):
                        gr.Markdown("### 🗣️ 2. Interactive Consultation")
                        question_box = gr.Textbox(
                            label="Ask your question",
                            placeholder="Ask about attendance shortage, exams, passing marks, revaluation fee, etc.",
                            max_lines=2
                        )
                        with gr.Row():
                            ask_btn = gr.Button("✨ Submit Search & Query", variant="primary")

                # Suggested Queries
                gr.Examples(
                    examples=[
                        "What is the minimum attendance requirement and the rules for shortage?",
                        "What are the rules, eligibility, and passing marks for examinations?",
                        "What are the scholarship criteria and the application deadline?",
                        "How do I request revaluation and what is the fee per script?",
                        "What is the address, site, and affiliation of the college?"
                    ],
                    inputs=question_box,
                    label="💡 Recommended Sample Compliance Questions"
                )

                gr.HTML("<br>")

                with gr.Column(elem_classes="beauty-card"):
                    gr.Markdown("### 🏉 AI Response & Source Verification")
                    with gr.Column(elem_classes="answer-card"):
                        answer_md = gr.Markdown(value="*Awaiting your question...*", label="Answer")
                    gr.HTML("<br>")
                    with gr.Accordion("🔍 View Context References & Similarity Metrics", open=False):
                        sources_html = gr.HTML("<p style='color: #64748b;'>No context chunks fetched yet.</p>")

    # Event Bindings
    login_btn.click(
        authenticate_student,
        inputs=[username_input, password_input],
        outputs=[login_container, main_portal_container, login_error]
    )
    password_input.submit(
        authenticate_student,
        inputs=[username_input, password_input],
        outputs=[login_container, main_portal_container, login_error]
    )

    pdf_input.upload(on_upload, inputs=pdf_input, outputs=status_md)
    sample_btn.click(lambda: build_knowledge_base(SAMPLE_PAGES, "Upgraded Academic Database"), outputs=status_md)

    ask_btn.click(on_ask, inputs=question_box, outputs=[answer_md, sources_html])
    question_box.submit(on_ask, inputs=question_box, outputs=[answer_md, sources_html])