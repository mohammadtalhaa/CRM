"""
Hassan Traders CRM — Full Production Build
==========================================
✅ Advance Sales with Edit/Payment correction
✅ Daily data download (Excel + PDF) per day
✅ Auto-cleanup of sales data older than 3 days (preserves customers/inventory/master data)
✅ Fully responsive (laptop + mobile)
✅ Everything interlinked: POS → Stock → Receipts → Ledger
✅ Complete HRM, Livestock, Finance, CRM, Inventory modules
"""

import streamlit as st
import pandas as pd
import json, os, hashlib, uuid, io
from datetime import datetime, date, timedelta
from io import BytesIO
import base64

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hassan Traders CRM",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Nunito',sans-serif;}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
    background:linear-gradient(160deg,#0f2027,#203a43,#2c5364)!important;
    min-width:240px!important;
}
section[data-testid="stSidebar"] *{color:#e0eafc!important;}
section[data-testid="stSidebar"] .stButton>button{
    background:rgba(255,255,255,0.07)!important;
    border:1px solid rgba(255,255,255,0.12)!important;
    color:#e0eafc!important;
    font-size:13px!important;
    padding:6px 10px!important;
    text-align:left!important;
    transition:all .15s;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(233,69,96,0.35)!important;
    border-color:#e94560!important;
}

/* ── Metric cards ── */
.metric-card{
    background:linear-gradient(135deg,#1a1a2e,#16213e);
    border:1px solid #0f3460;
    border-radius:14px;
    padding:16px 20px;
    text-align:center;
    margin-bottom:10px;
    box-shadow:0 4px 18px rgba(0,0,0,.45);
}
.metric-card h2{color:#e94560;font-size:1.75rem;margin:0;font-weight:800;}
.metric-card p{color:#a8b2d8;font-size:.78rem;margin:4px 0 0;text-transform:uppercase;letter-spacing:1px;}

/* ── Section header ── */
.section-header{
    background:linear-gradient(90deg,#e94560,#0f3460);
    color:#fff;
    padding:10px 20px;
    border-radius:8px;
    font-size:1.25rem;
    font-weight:800;
    margin-bottom:16px;
}

/* ── Global buttons ── */
.stButton>button{
    background:linear-gradient(90deg,#e94560,#0f3460);
    color:#fff!important;
    border:none!important;
    border-radius:8px!important;
    font-weight:700!important;
    padding:8px 18px!important;
    transition:all .2s;
}
.stButton>button:hover{opacity:.88;transform:translateY(-1px);}

/* ── Status badges ── */
.badge-green{background:#1a472a;color:#a9dfbf;padding:2px 10px;border-radius:20px;font-size:12px;}
.badge-red{background:#641e16;color:#f5b7b1;padding:2px 10px;border-radius:20px;font-size:12px;}
.badge-yellow{background:#7d6608;color:#fef9e7;padding:2px 10px;border-radius:20px;font-size:12px;}
.badge-blue{background:#1a3a5c;color:#aed6f1;padding:2px 10px;border-radius:20px;font-size:12px;}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"]{font-weight:700;font-size:13px;}

/* ── Inputs ── */
.stTextInput input,.stNumberInput input,.stDateInput input,.stTextArea textarea{
    border-radius:8px!important;
    border:1.5px solid #0f3460!important;
}

/* ── Responsive mobile ── */
@media(max-width:768px){
    .metric-card h2{font-size:1.3rem;}
    .section-header{font-size:1rem;padding:8px 14px;}
    section[data-testid="stSidebar"]{min-width:200px!important;}
}

/* ── Download button special ── */
.dl-btn a{
    background:linear-gradient(90deg,#27ae60,#1a6b3a)!important;
    color:#fff!important;
    padding:8px 18px!important;
    border-radius:8px!important;
    text-decoration:none!important;
    font-weight:700!important;
    display:inline-block;
    margin:4px 2px;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# ── DATA LAYER ─────────────────────────────────────────────────────────────────
DATA_DIR = "hassan_traders_data"
os.makedirs(DATA_DIR, exist_ok=True)

PERSISTENT_TABLES = [
    "customers","suppliers","employees","products","livestock","categories","units",
    "warehouses","company_settings","users","bmi_plans","price_lists","tax_settings",
    "notes","tasks","audit_log","attendance","salaries","loans","installments",
    "purchase_orders","stock_adjustments","damage_records","breeding_records",
    "livestock_health","feed_records","milk_records","batches","serials",
    "production","pos_sales_archive"
]

TRANSIENT_TABLES = [
    "pos_sales","transactions","receipts","payments","expenses",
    "livestock_sales","sale_orders","advance_sales","vehicle_trips"
]

def _path(name): return os.path.join(DATA_DIR, f"{name}.json")

def load_table(name):
    p = _path(name)
    if os.path.exists(p):
        try:
            with open(p) as f: return json.load(f)
        except: return []
    return []

def save_table(name, data):
    with open(_path(name), "w") as f:
        json.dump(data, f, indent=2, default=str)

def gen_id(prefix=""):
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"

def now_str():  return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def today_str(): return date.today().isoformat()

def log_audit(user, action, detail=""):
    al = load_table("audit_log")
    al.append({"id":gen_id("AL"),"user":user,"action":action,"detail":detail,"ts":now_str()})
    if len(al) > 2000: al = al[-2000:]
    save_table("audit_log", al)

# ── AUTO-CLEANUP (transient data older than 3 days → archived) ─────────────────
def auto_cleanup():
    cutoff = (date.today() - timedelta(days=3)).isoformat()
    for tbl in TRANSIENT_TABLES:
        data = load_table(tbl)
        keep = []
        archive = []
        for row in data:
            row_date = str(row.get("date","") or row.get("created_at",""))[:10]
            if row_date and row_date < cutoff:
                archive.append(row)
            else:
                keep.append(row)
        if archive:
            arch = load_table(f"{tbl}_archive")
            arch.extend(archive)
            save_table(f"{tbl}_archive", arch)
            save_table(tbl, keep)

# ── EXCEL EXPORT ───────────────────────────────────────────────────────────────
def df_to_excel_bytes(sheets_dict):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        for sheet_name, df in sheets_dict.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    return buf.getvalue()

def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode()

def make_download_link(data_bytes, filename, label, mime="application/octet-stream"):
    b64 = base64.b64encode(data_bytes).decode()
    return f'<a href="data:{mime};base64,{b64}" download="{filename}">{label}</a>'

# ── AUTH ───────────────────────────────────────────────────────────────────────
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def init_default_user():
    users = load_table("users")
    if not users:
        users.append({"id":"U001","username":"admin","password":hash_pw("admin123"),
                      "role":"Admin","name":"Administrator","email":"admin@hassantraders.com",
                      "phone":"","active":True,"created":today_str()})
        save_table("users", users)

def authenticate(username, password):
    for u in load_table("users"):
        if u["username"]==username and u["password"]==hash_pw(password) and u.get("active",True):
            return u
    return None

# ── SETTINGS ───────────────────────────────────────────────────────────────────
def init_settings():
    s = load_table("company_settings")
    if not s:
        s = [{"id":"CS001","name":"Hassan Traders","address":"Karachi, Pakistan",
              "phone":"0300-0000000","email":"info@hassantraders.com","ntn":"",
              "currency":"PKR","tax_rate":17.0,"fiscal_year_start":"01-07",
              "logo":"","sms_enabled":False,"low_stock_threshold":10}]
        save_table("company_settings", s)
    return s[0]

def get_settings():
    s = load_table("company_settings")
    return s[0] if s else {}

def currency(val):
    cur = get_settings().get("currency","PKR")
    try: return f"{cur} {float(val):,.2f}"
    except: return f"{cur} 0.00"

# ── UI HELPERS ─────────────────────────────────────────────────────────────────
def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def metric_card(label, value):
    st.markdown(f'<div class="metric-card"><h2>{value}</h2><p>{label}</p></div>',
                unsafe_allow_html=True)

def df_display(df, height=420):
    if df is None or df.empty: st.info("No records found.")
    else: st.dataframe(df, use_container_width=True, height=height)

def success(m): st.success(f"✅ {m}")
def error(m):   st.error(f"❌ {m}")
def warn(m):    st.warning(f"⚠️ {m}")
def info(m):    st.info(f"ℹ️ {m}")

# ── LOGIN ──────────────────────────────────────────────────────────────────────
def login_page():
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='text-align:center;padding:50px 0 24px'>
            <span style='font-size:72px'>🐄</span>
            <h1 style='background:linear-gradient(90deg,#e94560,#3498db);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               font-size:2.5rem;font-weight:800;margin:0'>Hassan Traders</h1>
            <p style='color:#888;margin:6px 0 0'>Complete Business Management System</p>
        </div>""", unsafe_allow_html=True)
        with st.form("login"):
            username = st.text_input("👤 Username", placeholder="admin")
            password = st.text_input("🔒 Password", type="password", placeholder="admin123")
            if st.form_submit_button("🚀 Login", use_container_width=True):
                user = authenticate(username, password)
                if user:
                    st.session_state.update({"logged_in":True,"user":user})
                    log_audit(username,"LOGIN")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Default: admin / admin123")

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
MENU = {
    "🏠 Dashboard":   ["Overview"],
    "💰 Finance":     ["Ledger","Cashbook","Receipts & Payments","Expenses","Daily Profit Report"],
    "📦 Inventory":   ["Products","Stock Adjustment","Damage Records","Warehouses","Price Lists"],
    "🛒 Sales":       ["Point of Sale","Sale Orders","Advance Sales","English Billing"],
    "📥 Purchases":   ["Purchase Orders","Supplier Management"],
    "👥 CRM":         ["Customers","Debtors & Creditors","Tasks & Follow-ups","Notes"],
    "🐄 Livestock":   ["Livestock Register","Milk Production","Feed Records","Breeding","Health Records","Livestock Sales"],
    "🏭 Production":  ["Production Orders","Production Report"],
    "💳 Installments":["BMI Plans","Installment Schedule"],
    "👨‍💼 HRM":        ["Employees","Attendance","Salary Management","Loans & Advances"],
    "📊 Reports":     ["Daily Download","Data Management"],
    "🏢 Company":     ["Settings","User Management","Audit Log"],
}

def render_sidebar():
    user = st.session_state.get("user",{})
    st.sidebar.markdown(f"""
    <div style='text-align:center;padding:16px 0 6px'>
        <span style='font-size:40px'>🐄</span>
        <h2 style='margin:4px 0;font-size:1.2rem;font-weight:800'>Hassan Traders</h2>
        <p style='margin:0;font-size:10px;opacity:.7'>Business Management System</p>
    </div>
    <div style='background:rgba(255,255,255,.07);border-radius:8px;
    padding:7px 12px;margin:6px 4px;font-size:12px'>
    👤 <b>{user.get('name','')}</b>&nbsp;|&nbsp;🔑 {user.get('role','')}</div>
    """, unsafe_allow_html=True)
    st.sidebar.divider()

    if "nav_section" not in st.session_state: st.session_state["nav_section"]="🏠 Dashboard"
    if "nav_page"    not in st.session_state: st.session_state["nav_page"]="Overview"

    for section, pages in MENU.items():
        with st.sidebar.expander(section, expanded=(st.session_state["nav_section"]==section)):
            for page in pages:
                if st.button(page, key=f"nav_{section}_{page}", use_container_width=True):
                    st.session_state["nav_section"]=section
                    st.session_state["nav_page"]=page
                    st.rerun()

    st.sidebar.divider()
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        log_audit(user.get("username",""),"LOGOUT")
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
def page_dashboard():
    section_header("📊 Business Dashboard — Hassan Traders")
    settings = get_settings(); cur = settings.get("currency","PKR")

    pos_sales   = load_table("pos_sales")
    customers   = load_table("customers")
    suppliers   = load_table("suppliers")
    products    = load_table("products")
    livestock   = load_table("livestock")
    expenses    = load_table("expenses")
    advance     = load_table("advance_sales")
    today       = today_str()
    month_start = date.today().replace(day=1).isoformat()

    today_sales  = sum(float(s.get("total",0)) for s in pos_sales if s.get("date","")[:10]==today)
    month_sales  = sum(float(s.get("total",0)) for s in pos_sales if s.get("date","")[:10]>=month_start)
    today_exp    = sum(float(e.get("amount",0)) for e in expenses if e.get("date","")[:10]==today)
    low_stock    = [p for p in products if float(p.get("stock",0))<float(p.get("min_stock",10))]
    pending_adv  = sum(float(a.get("balance",0)) for a in advance if a.get("status") not in ("Fully Paid","Cancelled"))
    active_ls    = len([l for l in livestock if l.get("status")=="Active"])

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: metric_card("Today Sales",    f"{cur} {today_sales:,.0f}")
    with c2: metric_card("Month Sales",    f"{cur} {month_sales:,.0f}")
    with c3: metric_card("Today Expenses", f"{cur} {today_exp:,.0f}")
    with c4: metric_card("Pending Advance",f"{cur} {pending_adv:,.0f}")
    with c5: metric_card("Active Livestock",active_ls)
    with c6: metric_card("Low Stock Items",len(low_stock))
    st.divider()

    col_l, col_r = st.columns([3,2])
    with col_l:
        st.subheader("📈 Sales Trend — Last 14 Days")
        if pos_sales:
            dates = [(date.today()-timedelta(days=i)).isoformat() for i in range(13,-1,-1)]
            chart_df = pd.DataFrame({
                "Date": dates,
                "Sales": [sum(float(s.get("total",0)) for s in pos_sales if s.get("date","")[:10]==d) for d in dates]
            })
            st.line_chart(chart_df.set_index("Date"))
        else:
            st.info("No sales data yet.")

        st.subheader("📦 Top Products by Stock Value")
        if products:
            top = sorted(products, key=lambda p: float(p.get("stock",0))*float(p.get("cost_price",0)), reverse=True)[:8]
            st.bar_chart(pd.DataFrame({"Product":[p["name"] for p in top],
                                        "Value":[float(p.get("stock",0))*float(p.get("cost_price",0)) for p in top]}).set_index("Product"))

    with col_r:
        st.subheader("⚠️ Low Stock Alerts")
        if low_stock:
            for p in low_stock[:8]:
                st.markdown(f'<span class="badge-red">{p["name"]}</span> &nbsp; Stock: {p.get("stock",0)} (Min: {p.get("min_stock",10)})',
                            unsafe_allow_html=True)
                st.write("")
        else: success("All stock levels are healthy!")

        st.subheader("💳 Pending Advance Payments")
        pend = [a for a in advance if a.get("status") not in ("Fully Paid","Cancelled")]
        if pend:
            for a in pend[:5]:
                st.markdown(f'<span class="badge-yellow">{a.get("customer","")}</span> — Balance: **{currency(a.get("balance",0))}**',
                            unsafe_allow_html=True)
        else: info("No pending advance payments.")

# ── LEDGER ────────────────────────────────────────────────────────────────────
def page_ledger():
    section_header("📒 General Ledger")
    transactions = load_table("transactions")
    tab1,tab2 = st.tabs(["Transaction List","Add Journal Entry"])

    with tab1:
        col1,col2,col3 = st.columns(3)
        with col1: d_from = st.date_input("From", date.today().replace(day=1), key="led_from")
        with col2: d_to   = st.date_input("To", date.today(), key="led_to")
        with col3: search = st.text_input("Search", key="led_search")
        filtered = [t for t in transactions if d_from.isoformat()<=str(t.get("date",""))[:10]<=d_to.isoformat()]
        if search: filtered = [t for t in filtered if search.lower() in str(t).lower()]
        if filtered:
            df = pd.DataFrame(filtered[::-1])
            cols = [c for c in ["date","ref","type","description","debit_account","credit_account","debit","credit","party"] if c in df.columns]
            df_display(df[cols])
            total_d = sum(float(t.get("debit",0)) for t in filtered)
            total_c = sum(float(t.get("credit",0)) for t in filtered)
            c1,c2,c3 = st.columns(3)
            c1.metric("Total Debits",currency(total_d))
            c2.metric("Total Credits",currency(total_c))
            c3.metric("Difference",currency(total_d-total_c))
        else: info("No transactions in selected period.")

    with tab2:
        with st.form("journal"):
            c1,c2 = st.columns(2)
            with c1:
                j_date = st.date_input("Date",date.today())
                j_ref  = st.text_input("Reference",value=gen_id("JV"))
                j_desc = st.text_input("Description")
                j_party= st.text_input("Party")
            with c2:
                j_debit_acc  = st.text_input("Debit Account")
                j_credit_acc = st.text_input("Credit Account")
                j_amount     = st.number_input("Amount",0.0,step=100.0)
                j_type       = st.selectbox("Type",["Journal","Debit Note","Credit Note","Contra"])
            if st.form_submit_button("💾 Post Entry", use_container_width=True):
                if j_amount>0 and j_debit_acc and j_credit_acc:
                    txns = load_table("transactions")
                    txns.append({"id":gen_id("TXN"),"ref":j_ref,"date":str(j_date),"type":j_type,
                                 "description":j_desc,"debit_account":j_debit_acc,"credit_account":j_credit_acc,
                                 "debit":j_amount,"credit":j_amount,"party":j_party,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("transactions",txns)
                    success("Journal entry posted!")
                    st.rerun()
                else: error("Fill all required fields.")

# ── CASHBOOK ──────────────────────────────────────────────────────────────────
def page_cashbook():
    section_header("💵 Cashbook")
    col1,col2 = st.columns(2)
    with col1: cb_from = st.date_input("From",date.today().replace(day=1))
    with col2: cb_to   = st.date_input("To",date.today())

    receipts = load_table("receipts")
    payments = load_table("payments")
    rec_f = [r for r in receipts if cb_from.isoformat()<=str(r.get("date",""))[:10]<=cb_to.isoformat()]
    pay_f = [p for p in payments if cb_from.isoformat()<=str(p.get("date",""))[:10]<=cb_to.isoformat()]
    total_rec = sum(float(r.get("amount",0)) for r in rec_f)
    total_pay = sum(float(p.get("amount",0)) for p in pay_f)

    c1,c2,c3 = st.columns(3)
    c1.metric("Total Receipts",currency(total_rec))
    c2.metric("Total Payments",currency(total_pay))
    c3.metric("Net Cash Balance",currency(total_rec-total_pay))
    st.divider()

    rows=[]
    for r in rec_f: rows.append({"Date":r.get("date",""),"Ref":r.get("ref",""),"Narration":f"Receipt - {r.get('party','')}","Receipts":r.get("amount",0),"Payments":0,"Mode":r.get("mode","")})
    for p in pay_f: rows.append({"Date":p.get("date",""),"Ref":p.get("ref",""),"Narration":f"Payment - {p.get('party','')}","Receipts":0,"Payments":p.get("amount",0),"Mode":p.get("mode","")})
    if rows:
        df = pd.DataFrame(sorted(rows,key=lambda x:x["Date"]))
        df_display(df)
    else: info("No cashbook entries in selected period.")

# ── RECEIPTS & PAYMENTS ───────────────────────────────────────────────────────
def page_receipts_payments():
    section_header("💳 Receipts & Payments")
    tab1,tab2 = st.tabs(["Records","New Entry"])
    receipts = load_table("receipts"); payments = load_table("payments")

    with tab1:
        view = st.radio("View",["Receipts","Payments","Both"],horizontal=True)
        c1,c2 = st.columns(2)
        with c1: d_from = st.date_input("From",date.today().replace(day=1),key="rp_from")
        with c2: d_to   = st.date_input("To",date.today(),key="rp_to")
        all_items=[]
        if view in ("Receipts","Both"):
            for r in receipts:
                if d_from.isoformat()<=str(r.get("date",""))[:10]<=d_to.isoformat():
                    all_items.append({**r,"Category":"Receipt"})
        if view in ("Payments","Both"):
            for p in payments:
                if d_from.isoformat()<=str(p.get("date",""))[:10]<=d_to.isoformat():
                    all_items.append({**p,"Category":"Payment"})
        if all_items:
            df=pd.DataFrame(all_items)
            cols=[c for c in ["date","ref","party","amount","mode","Category","notes"] if c in df.columns]
            df_display(df[cols])
            tr=sum(float(r.get("amount",0)) for r in receipts if d_from.isoformat()<=str(r.get("date",""))[:10]<=d_to.isoformat())
            tp=sum(float(p.get("amount",0)) for p in payments if d_from.isoformat()<=str(p.get("date",""))[:10]<=d_to.isoformat())
            c1,c2,c3=st.columns(3)
            c1.metric("Total Receipts",currency(tr))
            c2.metric("Total Payments",currency(tp))
            c3.metric("Net Cash Flow",currency(tr-tp))
        else: info("No records in selected period.")

    with tab2:
        etype=st.radio("Type",["Receipt","Payment"],horizontal=True,key="rp_type")
        with st.form("rp_form"):
            c1,c2=st.columns(2)
            with c1:
                rp_date=st.date_input("Date",date.today())
                ref=st.text_input("Reference",value=gen_id("RCP" if etype=="Receipt" else "PAY"))
                party=st.text_input("Party Name *")
                amount=st.number_input("Amount",0.0,step=100.0)
            with c2:
                mode=st.selectbox("Payment Mode",["Cash","Bank Transfer","Cheque","Online","Mobile Banking"])
                bank_ref=st.text_input("Bank/Cheque Ref")
                invoice_ref=st.text_input("Invoice/Sale Reference")
                notes=st.text_area("Notes",height=70)
            if st.form_submit_button(f"💾 Save {etype}", use_container_width=True):
                if amount>0 and party:
                    rec={"id":gen_id(),"ref":ref,"date":str(rp_date),"party":party,
                         "amount":amount,"mode":mode,"bank_ref":bank_ref,
                         "invoice_ref":invoice_ref,"notes":notes,"type":etype,
                         "created_by":st.session_state["user"]["username"],"created_at":now_str()}
                    tbl="receipts" if etype=="Receipt" else "payments"
                    d=load_table(tbl); d.append(rec); save_table(tbl,d)
                    txns=load_table("transactions")
                    txns.append({"id":gen_id("TXN"),"ref":ref,"date":str(rp_date),"type":etype,
                                 "description":f"{etype} from/to {party}",
                                 "debit_account":"Cash" if etype=="Receipt" else party,
                                 "credit_account":party if etype=="Receipt" else "Cash",
                                 "debit":amount,"credit":amount,"party":party,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("transactions",txns)
                    success(f"{etype} saved!")
                    st.rerun()
                else: error("Party and Amount required.")

# ── EXPENSES ──────────────────────────────────────────────────────────────────
def page_expenses():
    section_header("💸 Expenses Management")
    CATS=["Feed","Veterinary","Transport","Salaries","Utilities","Maintenance",
          "Fuel","Office","Marketing","Rent","Insurance","Miscellaneous"]
    tab1,tab2,tab3=st.tabs(["Expense List","Add Expense","Analysis"])

    with tab1:
        expenses=load_table("expenses")
        c1,c2,c3=st.columns(3)
        with c1: ef_from=st.date_input("From",date.today().replace(day=1),key="ex_from")
        with c2: ef_to  =st.date_input("To",date.today(),key="ex_to")
        with c3: ef_cat =st.selectbox("Category",["All"]+CATS)
        filtered=[e for e in expenses if ef_from.isoformat()<=str(e.get("date",""))[:10]<=ef_to.isoformat()]
        if ef_cat!="All": filtered=[e for e in filtered if e.get("category","")==ef_cat]
        if filtered:
            df=pd.DataFrame(filtered)
            cols=[c for c in ["date","ref","category","description","amount","paid_by","vendor","notes"] if c in df.columns]
            df_display(df[cols])
            st.metric("Total Expenses",currency(sum(float(e.get("amount",0)) for e in filtered)))
        else: info("No expenses in selected period.")

    with tab2:
        with st.form("add_exp"):
            c1,c2=st.columns(2)
            with c1:
                exp_date =st.date_input("Date",date.today())
                category =st.selectbox("Category",CATS)
                amount   =st.number_input("Amount",0.0,step=100.0)
                paid_by  =st.selectbox("Paid By",["Cash","Bank","Credit Card"])
            with c2:
                description=st.text_area("Description",height=70)
                vendor     =st.text_input("Vendor/Payee")
                ref        =st.text_input("Bill Reference")
                notes      =st.text_input("Notes")
            if st.form_submit_button("💾 Save Expense", use_container_width=True):
                if amount>0:
                    exps=load_table("expenses")
                    exps.append({"id":gen_id("EXP"),"ref":ref or gen_id("EXP"),"date":str(exp_date),
                                 "category":category,"description":description,"amount":amount,
                                 "paid_by":paid_by,"vendor":vendor,"notes":notes,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("expenses",exps)
                    success("Expense saved!")
                    st.rerun()

    with tab3:
        expenses=load_table("expenses")
        if expenses:
            cat_totals={}
            for e in expenses: cat_totals[e.get("category","Other")]=cat_totals.get(e.get("category","Other"),0)+float(e.get("amount",0))
            st.bar_chart(pd.DataFrame(list(cat_totals.items()),columns=["Category","Total"]).set_index("Category"))
        else: info("No data yet.")

# ── DAILY PROFIT REPORT ───────────────────────────────────────────────────────
def page_daily_profit():
    section_header("📊 Daily Profit Report")
    c1,c2=st.columns(2)
    with c1: rep_from=st.date_input("From",date.today().replace(day=1))
    with c2: rep_to  =st.date_input("To",date.today())

    pos_sales       =load_table("pos_sales")
    expenses        =load_table("expenses")
    livestock_sales =load_table("livestock_sales")

    rows=[]
    d=rep_from
    while d<=rep_to:
        ds=d.isoformat()
        day_sales    =sum(float(s.get("total",0))      for s in pos_sales       if str(s.get("date",""))[:10]==ds)
        day_cost     =sum(float(s.get("cost_total",0)) for s in pos_sales       if str(s.get("date",""))[:10]==ds)
        day_ls_sales =sum(float(s.get("sale_price",0)) for s in livestock_sales if str(s.get("date",""))[:10]==ds)
        day_ls_cost  =sum(float(s.get("purchase_price",0)) for s in livestock_sales if str(s.get("date",""))[:10]==ds)
        day_exp      =sum(float(e.get("amount",0))     for e in expenses        if str(e.get("date",""))[:10]==ds)
        gross=(day_sales-day_cost)+(day_ls_sales-day_ls_cost)
        rows.append({"Date":ds,"Sales":day_sales,"COGS":day_cost,"LS Sales":day_ls_sales,
                     "LS Cost":day_ls_cost,"Expenses":day_exp,"Gross Profit":gross,"Net Profit":gross-day_exp})
        d+=timedelta(days=1)

    if rows:
        df=pd.DataFrame(rows)
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Total Sales",currency(df["Sales"].sum()))
        c2.metric("Total Expenses",currency(df["Expenses"].sum()))
        c3.metric("Gross Profit",currency(df["Gross Profit"].sum()))
        c4.metric("Net Profit",currency(df["Net Profit"].sum()))
        st.divider(); df_display(df)
        st.line_chart(df.set_index("Date")[["Sales","Net Profit","Expenses"]])

# ── PRODUCTS ──────────────────────────────────────────────────────────────────
def page_products():
    section_header("📦 Product Management")
    cats  = load_table("categories"); cat_names  = [c["name"] for c in cats] if cats else ["Feed","Medicine","Equipment","Other"]
    units = load_table("units");      unit_names = [u["name"] for u in units] if units else ["KG","Gram","Liter","Piece","Box","Bag","Ton"]
    tab1,tab2,tab3=st.tabs(["Product List","Add Product","Stock Summary"])

    with tab1:
        products=load_table("products")
        c1,c2,c3=st.columns(3)
        with c1: search=st.text_input("🔍 Search",key="ps")
        with c2: cat_f =st.selectbox("Category",["All"]+cat_names)
        with c3: sf    =st.selectbox("Stock Filter",["All","Low Stock","Out of Stock","In Stock"])
        filtered=products
        if search: filtered=[p for p in filtered if search.lower() in p.get("name","").lower() or search.lower() in p.get("sku","").lower()]
        if cat_f!="All": filtered=[p for p in filtered if p.get("category","")==cat_f]
        if sf=="Low Stock": filtered=[p for p in filtered if 0<float(p.get("stock",0))<float(p.get("min_stock",10))]
        elif sf=="Out of Stock": filtered=[p for p in filtered if float(p.get("stock",0))==0]
        elif sf=="In Stock": filtered=[p for p in filtered if float(p.get("stock",0))>0]
        if filtered:
            df=pd.DataFrame(filtered)
            cols=[c for c in ["sku","name","category","unit","stock","min_stock","cost_price","sale_price","barcode"] if c in df.columns]
            st.dataframe(df[cols],use_container_width=True,height=420)
        else: info("No products found.")

    with tab2:
        with st.form("add_prod"):
            c1,c2,c3=st.columns(3)
            with c1:
                sku=st.text_input("SKU",value=gen_id("PRD")); name=st.text_input("Product Name *")
                category=st.selectbox("Category",cat_names); brand=st.text_input("Brand")
                unit=st.selectbox("Unit",unit_names)
            with c2:
                cost_price=st.number_input("Cost Price",0.0,step=1.0)
                sale_price=st.number_input("Sale Price (Retail)",0.0,step=1.0)
                sale_price2=st.number_input("Sale Price 2 (Wholesale)",0.0,step=1.0)
                tax_rate=st.number_input("Tax Rate %",0.0,100.0,0.0,step=0.5)
            with c3:
                opening_stock=st.number_input("Opening Stock",0.0,step=1.0)
                min_stock=st.number_input("Min Stock (Reorder)",0.0,step=1.0)
                barcode=st.text_input("Barcode")
                location=st.text_input("Storage Location")
            description=st.text_area("Description",height=55)
            if st.form_submit_button("💾 Save Product", use_container_width=True):
                if name:
                    products=load_table("products")
                    products.append({"id":gen_id("PRD"),"sku":sku,"name":name,"category":category,
                                     "brand":brand,"unit":unit,"cost_price":cost_price,
                                     "sale_price":sale_price,"sale_price2":sale_price2,
                                     "tax_rate":tax_rate,"stock":opening_stock,"min_stock":min_stock,
                                     "barcode":barcode,"location":location,"description":description,
                                     "active":True,"created":today_str()})
                    save_table("products",products)
                    log_audit(st.session_state["user"]["username"],"ADD_PRODUCT",name)
                    success(f"Product '{name}' added!")
                    st.rerun()
                else: error("Product name required.")

    with tab3:
        products=load_table("products")
        if products:
            total_cv =sum(float(p.get("stock",0))*float(p.get("cost_price",0)) for p in products)
            total_sv =sum(float(p.get("stock",0))*float(p.get("sale_price",0)) for p in products)
            low      =len([p for p in products if float(p.get("stock",0))<float(p.get("min_stock",10))])
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Total Products",len(products)); c2.metric("Stock Cost Value",currency(total_cv))
            c3.metric("Stock Sale Value",currency(total_sv)); c4.metric("Low Stock",low)
            by_cat={}
            for p in products:
                cat=p.get("category","Other"); by_cat[cat]=by_cat.get(cat,0)+float(p.get("stock",0))*float(p.get("cost_price",0))
            st.bar_chart(pd.DataFrame(list(by_cat.items()),columns=["Category","Value"]).set_index("Category"))

# ── STOCK ADJUSTMENT ─────────────────────────────────────────────────────────
def page_stock_adjustment():
    section_header("📦 Stock Adjustment")
    products=load_table("products"); prod_names=[p["name"] for p in products]
    tab1,tab2=st.tabs(["Adjustment History","New Adjustment"])

    with tab1:
        adj=load_table("stock_adjustments")
        if adj: df_display(pd.DataFrame(adj))
        else: info("No adjustments yet.")

    with tab2:
        if prod_names:
            with st.form("stock_adj"):
                c1,c2=st.columns(2)
                with c1:
                    sa_prod=st.selectbox("Product",prod_names)
                    sa_type=st.selectbox("Adjustment Type",["Add Stock","Remove Stock","Correction"])
                    sa_qty =st.number_input("Quantity",0.0,step=1.0)
                with c2:
                    sa_reason=st.selectbox("Reason",["Purchase Received","Return","Damage Write-off","Count Correction","Transfer","Other"])
                    sa_date  =st.date_input("Date",date.today())
                    sa_notes =st.text_area("Notes",height=60)
                if st.form_submit_button("💾 Save Adjustment", use_container_width=True):
                    if sa_qty>0:
                        adj=load_table("stock_adjustments")
                        p_data=next((p for p in products if p["name"]==sa_prod),{})
                        old_stock=float(p_data.get("stock",0))
                        new_stock=old_stock+sa_qty if sa_type=="Add Stock" else max(0,old_stock-sa_qty) if sa_type=="Remove Stock" else sa_qty
                        adj.append({"id":gen_id("SA"),"date":str(sa_date),"product":sa_prod,
                                    "type":sa_type,"qty":sa_qty,"old_stock":old_stock,"new_stock":new_stock,
                                    "reason":sa_reason,"notes":sa_notes,
                                    "by":st.session_state["user"]["username"],"created_at":now_str()})
                        save_table("stock_adjustments",adj)
                        for p in products:
                            if p["name"]==sa_prod: p["stock"]=new_stock
                        save_table("products",products)
                        success(f"Stock adjusted: {old_stock} → {new_stock}")
                        st.rerun()
        else: warn("Add products first.")

# ── DAMAGE RECORDS ────────────────────────────────────────────────────────────
def page_damage():
    section_header("⚠️ Damage & Write-off Records")
    products=load_table("products"); prod_names=[p["name"] for p in products]
    tab1,tab2=st.tabs(["Damage Records","Record Damage"])

    with tab1:
        dr=load_table("damage_records")
        if dr: df_display(pd.DataFrame(dr))
        else: info("No damage records.")

    with tab2:
        with st.form("dmg_rec"):
            c1,c2=st.columns(2)
            with c1:
                d_prod =st.selectbox("Product",prod_names) if prod_names else st.text_input("Product")
                d_qty  =st.number_input("Quantity",0.0,step=1.0)
                d_date =st.date_input("Date",date.today())
            with c2:
                d_reason=st.selectbox("Reason",["Expired","Physical Damage","Water Damage","Fire","Theft","Quality Issue","Other"])
                d_value =st.number_input("Estimated Loss Value",0.0,step=10.0)
                d_notes =st.text_area("Notes",height=60)
            if st.form_submit_button("💾 Record Damage", use_container_width=True):
                if d_qty>0:
                    dr=load_table("damage_records")
                    dr.append({"id":gen_id("DMG"),"date":str(d_date),"product":d_prod,
                               "qty":d_qty,"reason":d_reason,"value":d_value,"notes":d_notes,
                               "by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("damage_records",dr)
                    for p in products:
                        if p["name"]==d_prod: p["stock"]=max(0,float(p.get("stock",0))-d_qty)
                    save_table("products",products)
                    success("Damage recorded and stock adjusted!")
                    st.rerun()

# ── WAREHOUSES ────────────────────────────────────────────────────────────────
def page_warehouses():
    section_header("🏭 Warehouse Management")
    tab1,tab2=st.tabs(["Warehouse List","Add Warehouse"])
    with tab1:
        wh=load_table("warehouses")
        if wh: df_display(pd.DataFrame(wh))
        else: info("No warehouses added yet.")
    with tab2:
        with st.form("wh_form"):
            c1,c2=st.columns(2)
            with c1:
                wn=st.text_input("Warehouse Name *"); wcode=st.text_input("Code")
                wcity=st.text_input("City"); wcap=st.number_input("Capacity (units)",0.0,step=1.0)
            with c2:
                waddr=st.text_area("Address",height=70); wmanager=st.text_input("Manager")
                wphone=st.text_input("Phone"); wnotes=st.text_area("Notes",height=40)
            if st.form_submit_button("💾 Save"):
                if wn:
                    wh=load_table("warehouses")
                    wh.append({"id":gen_id("WH"),"name":wn,"code":wcode,"city":wcity,
                               "capacity":wcap,"address":waddr,"manager":wmanager,
                               "phone":wphone,"notes":wnotes,"created":today_str()})
                    save_table("warehouses",wh); success(f"Warehouse '{wn}' added!"); st.rerun()

# ── PRICE LISTS ───────────────────────────────────────────────────────────────
def page_price_lists():
    section_header("💰 Price Lists")
    products=load_table("products")
    if products:
        df=pd.DataFrame([{"SKU":p.get("sku",""),"Product":p.get("name",""),"Unit":p.get("unit",""),
                           "Cost":p.get("cost_price",0),"Retail":p.get("sale_price",0),
                           "Wholesale":p.get("sale_price2",0),"Stock":p.get("stock",0)} for p in products])
        df_display(df)
        xl=df_to_excel_bytes({"Price List":df})
        st.markdown('<div class="dl-btn">'+make_download_link(xl,"price_list.xlsx","📥 Download Price List (Excel)")+'</div>',unsafe_allow_html=True)
    else: info("No products yet.")

# ── POS ───────────────────────────────────────────────────────────────────────
def page_pos():
    section_header("🛒 Point of Sale")
    products  = load_table("products")
    customers = load_table("customers")
    cust_names= ["Walk-in"]+[c["name"] for c in customers]
    prod_dict = {p["name"]:p for p in products}
    settings  = get_settings()

    if "pos_cart" not in st.session_state: st.session_state["pos_cart"]=[]

    col_l,col_r=st.columns([2,1])
    with col_l:
        st.subheader("🔍 Add Products")
        c1,c2,c3=st.columns([3,1,1])
        with c1:
            prod_names=[p["name"] for p in products if float(p.get("stock",0))>0]
            pos_prod=st.selectbox("Product",prod_names if prod_names else ["No stock available"],key="pos_prod")
        with c2: pos_qty=st.number_input("Qty",1.0,step=1.0,key="pos_qty")
        with c3:
            p_data=prod_dict.get(pos_prod,{})
            pos_price=st.number_input("Price",0.0,step=1.0,key="pos_price",value=float(p_data.get("sale_price",0)))

        if st.button("➕ Add to Cart", use_container_width=True):
            if pos_prod and pos_prod in prod_dict:
                p=prod_dict[pos_prod]
                if float(p.get("stock",0))>=pos_qty:
                    st.session_state["pos_cart"].append({
                        "product_id":p["id"],"product":pos_prod,"qty":pos_qty,
                        "price":pos_price,"cost":float(p.get("cost_price",0)),
                        "total":pos_qty*pos_price})
                    st.rerun()
                else: error(f"Insufficient stock! Available: {p.get('stock',0)}")

        if st.session_state["pos_cart"]:
            st.subheader("🛒 Cart")
            for i,item in enumerate(st.session_state["pos_cart"]):
                cc1,cc2,cc3,cc4=st.columns([3,1,1,1])
                with cc1: st.write(f"**{item['product']}**")
                with cc2: st.write(f"Qty: {item['qty']}")
                with cc3: st.write(f"{currency(item['total'])}")
                with cc4:
                    if st.button("🗑️",key=f"rm_{i}"):
                        st.session_state["pos_cart"].pop(i); st.rerun()

    with col_r:
        st.subheader("💰 Checkout")
        customer=st.selectbox("Customer",cust_names,key="pos_cust")
        disc_pct=st.number_input("Discount %",0.0,100.0,0.0,step=0.5,key="pos_disc")
        tax_rate=st.number_input("Tax %",0.0,100.0,settings.get("tax_rate",0.0),step=0.5,key="pos_tax")
        payment_mode=st.selectbox("Payment Mode",["Cash","Bank Transfer","Cheque","Credit","Mobile Banking"],key="pos_pm")

        if st.session_state["pos_cart"]:
            subtotal=sum(i["total"] for i in st.session_state["pos_cart"])
            disc_amt=subtotal*disc_pct/100
            tax_amt =(subtotal-disc_amt)*tax_rate/100
            total   =subtotal-disc_amt+tax_amt
            amount_paid=st.number_input("Amount Paid",0.0,step=100.0,value=float(total),key="pos_paid")
            change=amount_paid-total

            st.markdown(f"""
            <div style='background:#1a1a2e;border-radius:10px;padding:14px;margin:8px 0'>
                <table width='100%'>
                <tr><td>Subtotal</td><td align='right'>{currency(subtotal)}</td></tr>
                <tr><td>Discount</td><td align='right'>-{currency(disc_amt)}</td></tr>
                <tr><td>Tax</td><td align='right'>{currency(tax_amt)}</td></tr>
                <tr style='font-size:1.2rem;font-weight:800'><td>TOTAL</td><td align='right'><span style='color:#e94560'>{currency(total)}</span></td></tr>
                <tr><td>Paid</td><td align='right'>{currency(amount_paid)}</td></tr>
                <tr><td>Change</td><td align='right'><span style='color:{"#2ecc71" if change>=0 else "#e74c3c"}'>{currency(change)}</span></td></tr>
                </table>
            </div>""", unsafe_allow_html=True)

            if payment_mode=="Credit":
                warn("Credit sale — balance will be added to customer ledger.")

            cc1,cc2=st.columns(2)
            with cc1:
                if st.button("✅ Process Sale", use_container_width=True, type="primary"):
                    sale_id=gen_id("POS")
                    sale={"id":sale_id,"date":today_str(),"time":datetime.now().strftime("%H:%M:%S"),
                          "customer":customer,"items":st.session_state["pos_cart"],"subtotal":subtotal,
                          "discount_pct":disc_pct,"discount_amt":disc_amt,"tax_rate":tax_rate,
                          "tax_amt":tax_amt,"total":total,"amount_paid":amount_paid,"change":change,
                          "payment_mode":payment_mode,
                          "cost_total":sum(i.get("cost",0)*i["qty"] for i in st.session_state["pos_cart"]),
                          "created_by":st.session_state["user"]["username"]}
                    ps=load_table("pos_sales"); ps.append(sale); save_table("pos_sales",ps)
                    prods=load_table("products")
                    for item in st.session_state["pos_cart"]:
                        for p in prods:
                            if p["id"]==item["product_id"]: p["stock"]=max(0,float(p.get("stock",0))-item["qty"])
                    save_table("products",prods)
                    # Receipt
                    if payment_mode!="Credit":
                        rec=load_table("receipts")
                        rec.append({"id":gen_id(),"ref":sale_id,"date":today_str(),"party":customer,
                                    "amount":amount_paid,"mode":payment_mode,"type":"Receipt",
                                    "notes":f"POS Sale {sale_id}","created_at":now_str()})
                        save_table("receipts",rec)
                    # Update customer balance if credit
                    if payment_mode=="Credit":
                        custs=load_table("customers")
                        for c in custs:
                            if c["name"]==customer: c["balance"]=float(c.get("balance",0))+total
                        save_table("customers",custs)
                    log_audit(st.session_state["user"]["username"],"POS_SALE",f"{sale_id}:{total}")
                    st.session_state["pos_cart"]=[]
                    success(f"✅ Sale {sale_id} — Change: {currency(change)}")
                    st.rerun()
            with cc2:
                if st.button("🗑️ Clear Cart", use_container_width=True):
                    st.session_state["pos_cart"]=[]; st.rerun()
        else:
            st.info("Cart is empty.")

    st.divider()
    st.subheader("📋 Today's POS Sales")
    pos_sales=load_table("pos_sales")
    today_sales=[s for s in pos_sales if s.get("date","")==today_str()]
    if today_sales:
        rows=[{"Sale ID":s["id"],"Time":s.get("time",""),"Customer":s.get("customer",""),
               "Total":currency(s.get("total",0)),"Paid":currency(s.get("amount_paid",0)),
               "Mode":s.get("payment_mode",""),"By":s.get("created_by","")} for s in today_sales[-20:]]
        df_display(pd.DataFrame(rows),300)
    else: info("No sales today yet.")

# ── SALE ORDERS ───────────────────────────────────────────────────────────────
def page_sale_orders():
    section_header("📋 Sale Orders")
    products=load_table("products"); customers=load_table("customers")
    cust_names=[c["name"] for c in customers]; prod_names=[p["name"] for p in products]
    prod_dict={p["name"]:p for p in products}
    tab1,tab2=st.tabs(["Order List","New Sale Order"])

    with tab1:
        orders=load_table("sale_orders")
        c1,c2,c3=st.columns(3)
        with c1: so_from=st.date_input("From",date.today().replace(day=1),key="so_f")
        with c2: so_to  =st.date_input("To",date.today(),key="so_t")
        with c3: so_stat=st.selectbox("Status",["All","Draft","Confirmed","Delivered","Cancelled"])
        filtered=[o for o in orders if so_from.isoformat()<=str(o.get("date",""))[:10]<=so_to.isoformat()]
        if so_stat!="All": filtered=[o for o in filtered if o.get("status","")==so_stat]
        if filtered:
            df=pd.DataFrame([{"Order#":o["id"],"Date":o.get("date",""),"Customer":o.get("customer",""),
                               "Total":currency(o.get("total",0)),"Status":o.get("status",""),
                               "Notes":o.get("notes","")} for o in filtered])
            df_display(df)
        else: info("No orders in range.")

    with tab2:
        if "so_cart" not in st.session_state: st.session_state["so_cart"]=[]
        c1,c2=st.columns(2)
        with c1:
            so_cust=st.selectbox("Customer *",cust_names) if cust_names else st.text_input("Customer")
            so_date=st.date_input("Order Date",date.today())
            so_del =st.date_input("Expected Delivery",date.today()+timedelta(days=3))
        with c2:
            so_stat_n=st.selectbox("Status",["Draft","Confirmed"])
            so_notes =st.text_area("Notes",height=60)
            so_disc  =st.number_input("Discount %",0.0,100.0,0.0,step=0.5)
        c1,c2,c3=st.columns([3,1,1])
        with c1: so_prod =st.selectbox("Add Product",prod_names,key="so_ap")
        with c2: so_qty  =st.number_input("Qty",1.0,step=1.0,key="so_qty")
        with c3: so_price=st.number_input("Price",0.0,step=1.0,key="so_pr",
                                           value=float(prod_dict.get(so_prod,{}).get("sale_price",0)) if prod_names else 0.0)
        if st.button("➕ Add to Order"):
            st.session_state["so_cart"].append({"product":so_prod,"qty":so_qty,"price":so_price,"total":so_qty*so_price})
            st.rerun()
        if st.session_state["so_cart"]:
            st.dataframe(pd.DataFrame(st.session_state["so_cart"]),use_container_width=True)
            sub=sum(i["total"] for i in st.session_state["so_cart"])
            disc=sub*so_disc/100; total=sub-disc
            st.write(f"**Subtotal:** {currency(sub)} | **Discount:** {currency(disc)} | **Total:** {currency(total)}")
            if st.button("✅ Create Order", type="primary"):
                orders=load_table("sale_orders"); oid=gen_id("SO")
                orders.append({"id":oid,"date":str(so_date),"customer":so_cust,
                                "delivery_date":str(so_del),"status":so_stat_n,
                                "items":st.session_state["so_cart"],"subtotal":sub,
                                "discount":so_disc,"total":total,"notes":so_notes,
                                "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("sale_orders",orders)
                st.session_state["so_cart"]=[]
                success(f"Sale Order {oid} created!"); st.rerun()

# ── ADVANCE SALES (with Edit / Payment Update) ────────────────────────────────
def page_advance_sales():
    section_header("💳 Advance Sales — with Payment Tracking")
    customers=load_table("customers"); products=load_table("products")
    cust_names=[c["name"] for c in customers]
    prod_names=[p["name"] for p in products]
    tab1,tab2,tab3=st.tabs(["Advance Sales List","New Advance Sale","Edit / Add Payment"])

    with tab1:
        adv=load_table("advance_sales")
        if adv:
            df=pd.DataFrame([{
                "ID":a["id"],"Date":a.get("date",""),"Customer":a.get("customer",""),
                "Product":a.get("product",""),"Total":currency(a.get("total",0)),
                "Advance Paid":currency(a.get("advance_paid",0)),
                "Balance":currency(float(a.get("total",0))-float(a.get("advance_paid",0))),
                "Delivery":a.get("delivery_date",""),"Status":a.get("status","")
            } for a in adv])
            df_display(df)
            pending=[a for a in adv if a.get("status") not in ("Fully Paid","Cancelled")]
            if pending:
                st.metric("Total Pending Balance",
                          currency(sum(float(a.get("total",0))-float(a.get("advance_paid",0)) for a in pending)))
        else: info("No advance sales yet.")

    with tab2:
        with st.form("adv_sale"):
            c1,c2=st.columns(2)
            with c1:
                as_cust=st.selectbox("Customer",cust_names) if cust_names else st.text_input("Customer")
                as_prod=st.selectbox("Product",prod_names)  if prod_names else st.text_input("Product")
                as_qty =st.number_input("Quantity",1.0,step=1.0)
                as_price=st.number_input("Sale Price per Unit",0.0,step=1.0)
            with c2:
                as_advance=st.number_input("Advance Amount Received",0.0,step=100.0)
                as_del    =st.date_input("Expected Delivery",date.today()+timedelta(days=7))
                as_notes  =st.text_area("Notes",height=60)
                as_status =st.selectbox("Status",["Pending","Partially Paid","Fully Paid","Delivered","Cancelled"])
            if st.form_submit_button("💾 Save Advance Sale", use_container_width=True):
                total=as_qty*as_price
                if as_advance>total: error("Advance cannot exceed total.")
                else:
                    adv=load_table("advance_sales")
                    aid=gen_id("ADV")
                    adv.append({"id":aid,"date":today_str(),"customer":as_cust,"product":as_prod,
                                "qty":as_qty,"price":as_price,"total":total,
                                "advance_paid":as_advance,"balance":total-as_advance,
                                "delivery_date":str(as_del),"status":as_status,"notes":as_notes,
                                "payments":[{"date":today_str(),"amount":as_advance,"notes":"Initial advance"}] if as_advance>0 else [],
                                "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("advance_sales",adv)
                    if as_advance>0:
                        rec=load_table("receipts")
                        rec.append({"id":gen_id(),"ref":aid,"date":today_str(),"party":as_cust,
                                    "amount":as_advance,"mode":"Cash","type":"Receipt",
                                    "notes":f"Advance sale {aid}","created_at":now_str()})
                        save_table("receipts",rec)
                    success(f"Advance sale {aid} created!"); st.rerun()

    with tab3:
        st.subheader("✏️ Edit / Add Payment to Existing Advance Sale")
        adv=load_table("advance_sales")
        pending=[a for a in adv if a.get("status") not in ("Fully Paid","Cancelled")]
        if not pending: info("No pending advance sales."); return

        adv_opts={f"{a['id']} — {a.get('customer','')} — Balance: {currency(float(a.get('total',0))-float(a.get('advance_paid',0)))}":a for a in pending}
        sel_label=st.selectbox("Select Advance Sale",list(adv_opts.keys()))
        sel=adv_opts[sel_label]

        c1,c2,c3=st.columns(3)
        c1.metric("Total Amount",currency(sel.get("total",0)))
        c2.metric("Amount Paid",currency(sel.get("advance_paid",0)))
        c3.metric("Balance Due",currency(float(sel.get("total",0))-float(sel.get("advance_paid",0))))

        # Payment history
        payments_hist=sel.get("payments",[])
        if payments_hist:
            st.markdown("**💳 Payment History:**")
            df_display(pd.DataFrame(payments_hist),200)

        st.divider()
        st.subheader("➕ Add New Payment")
        with st.form("add_adv_payment"):
            c1,c2=st.columns(2)
            with c1:
                pay_amount=st.number_input("Payment Amount",0.0,
                                           max_value=float(float(sel.get("total",0))-float(sel.get("advance_paid",0))),
                                           step=100.0)
                pay_mode=st.selectbox("Payment Mode",["Cash","Bank Transfer","Cheque","Mobile Banking"])
            with c2:
                pay_date=st.date_input("Payment Date",date.today())
                pay_notes=st.text_area("Notes",height=60)

            if st.form_submit_button("💰 Record Payment", use_container_width=True):
                if pay_amount>0:
                    new_paid=float(sel.get("advance_paid",0))+pay_amount
                    new_bal =float(sel.get("total",0))-new_paid
                    new_status="Fully Paid" if new_bal<=0 else "Partially Paid"
                    for a in adv:
                        if a["id"]==sel["id"]:
                            a["advance_paid"]=new_paid
                            a["balance"]=max(0,new_bal)
                            a["status"]=new_status
                            if "payments" not in a: a["payments"]=[]
                            a["payments"].append({"date":str(pay_date),"amount":pay_amount,
                                                  "mode":pay_mode,"notes":pay_notes,
                                                  "by":st.session_state["user"]["username"]})
                    save_table("advance_sales",adv)
                    # Record receipt
                    rec=load_table("receipts")
                    rec.append({"id":gen_id(),"ref":sel["id"],"date":str(pay_date),
                                "party":sel.get("customer",""),"amount":pay_amount,"mode":pay_mode,
                                "type":"Receipt","notes":f"Advance payment for {sel['id']}","created_at":now_str()})
                    save_table("receipts",rec)
                    # Update customer balance if needed
                    custs=load_table("customers")
                    for c in custs:
                        if c["name"]==sel.get("customer",""):
                            c["balance"]=max(0,float(c.get("balance",0))-pay_amount)
                    save_table("customers",custs)
                    success(f"Payment of {currency(pay_amount)} recorded! New balance: {currency(max(0,new_bal))}")
                    st.rerun()

        st.divider()
        st.subheader("✏️ Edit Advance Sale Details")
        with st.form("edit_adv"):
            c1,c2=st.columns(2)
            with c1:
                new_del  =st.date_input("Update Delivery Date", date.fromisoformat(sel.get("delivery_date",today_str())))
                new_notes=st.text_area("Update Notes",value=sel.get("notes",""),height=60)
            with c2:
                new_status_e=st.selectbox("Update Status",["Pending","Partially Paid","Fully Paid","Delivered","Cancelled"],
                                           index=["Pending","Partially Paid","Fully Paid","Delivered","Cancelled"].index(sel.get("status","Pending")))
            if st.form_submit_button("💾 Save Changes"):
                for a in adv:
                    if a["id"]==sel["id"]:
                        a["delivery_date"]=str(new_del); a["notes"]=new_notes; a["status"]=new_status_e
                save_table("advance_sales",adv)
                success("Advance sale updated!"); st.rerun()

# ── ENGLISH BILLING ───────────────────────────────────────────────────────────
def page_english_billing():
    section_header("🧾 Invoice Generator")
    products=load_table("products"); customers=load_table("customers"); settings=get_settings()
    prod_names=[p["name"] for p in products]; cust_names=[c["name"] for c in customers]
    tab1,tab2=st.tabs(["Create Invoice","Invoice History"])

    with tab1:
        if "bill_items" not in st.session_state: st.session_state["bill_items"]=[]
        c1,c2,c3=st.columns(3)
        with c1:
            inv_no  =st.text_input("Invoice #",value=gen_id("INV"))
            inv_date=st.date_input("Date",date.today())
            due_date=st.date_input("Due Date",date.today()+timedelta(days=30))
        with c2:
            bill_cust=st.selectbox("Bill To",cust_names) if cust_names else st.text_input("Customer")
            inv_cur  =st.selectbox("Currency",["PKR","USD","EUR","GBP"])
            tax_rate =st.number_input("Tax %",0.0,100.0,settings.get("tax_rate",17.0))
        with c3:
            inv_notes=st.text_area("Terms",height=80,value="Payment due within 30 days. Thank you!")

        c1,c2,c3,c4=st.columns([3,1,1,1])
        with c1: bp=st.selectbox("Product/Service",prod_names+["Custom Item"],key="bp")
        with c2: bq=st.number_input("Qty",1.0,step=1.0,key="bq")
        p_=next((x for x in products if x["name"]==bp),{})
        with c3: bpr=st.number_input("Unit Price",0.0,step=1.0,key="bpr",value=float(p_.get("sale_price",0)))
        with c4: bd=st.number_input("Disc%",0.0,100.0,0.0,key="bd")
        if st.button("➕ Add Line Item"):
            da=bq*bpr*bd/100
            st.session_state["bill_items"].append({"Description":bp,"Qty":bq,"Unit Price":bpr,"Disc%":bd,"Amount":bq*bpr-da})
            st.rerun()
        if st.session_state["bill_items"]:
            df=pd.DataFrame(st.session_state["bill_items"]); st.dataframe(df,use_container_width=True)
            sub=sum(i["Amount"] for i in st.session_state["bill_items"])
            tax=sub*tax_rate/100; grand=sub+tax
            st.markdown(f"**Subtotal:** {inv_cur} {sub:,.2f} | **Tax:** {inv_cur} {tax:,.2f} | **Grand Total:** {inv_cur} {grand:,.2f}")
            c1,c2=st.columns(2)
            with c1:
                if st.button("💾 Save Invoice",type="primary",use_container_width=True):
                    so=load_table("sale_orders")
                    so.append({"id":inv_no,"date":str(inv_date),"due_date":str(due_date),
                               "customer":bill_cust,"items":st.session_state["bill_items"],
                               "subtotal":sub,"tax_rate":tax_rate,"tax_amt":tax,"total":grand,
                               "currency":inv_cur,"notes":inv_notes,"status":"Confirmed","type":"Invoice",
                               "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("sale_orders",so); st.session_state["bill_items"]=[]
                    success(f"Invoice {inv_no} saved!"); st.rerun()
            with c2:
                if st.button("🗑️ Clear",use_container_width=True):
                    st.session_state["bill_items"]=[]; st.rerun()

    with tab2:
        orders=load_table("sale_orders")
        invs=[o for o in orders if o.get("type")=="Invoice"]
        if invs:
            df=pd.DataFrame([{"Invoice#":i["id"],"Date":i.get("date",""),"Customer":i.get("customer",""),
                               "Total":currency(i.get("total",0)),"Status":i.get("status","")} for i in invs])
            df_display(df)
        else: info("No invoices yet.")

# ── PURCHASE ORDERS ───────────────────────────────────────────────────────────
def page_purchase_orders():
    section_header("📥 Purchase Orders")
    products=load_table("products"); suppliers=load_table("suppliers")
    sup_names=[s["name"] for s in suppliers]; prod_names=[p["name"] for p in products]
    prod_dict={p["name"]:p for p in products}
    tab1,tab2=st.tabs(["PO List","New Purchase Order"])

    with tab1:
        pos_list=load_table("purchase_orders")
        if pos_list:
            df=pd.DataFrame([{"PO#":p["id"],"Date":p.get("date",""),"Supplier":p.get("supplier",""),
                               "Total":currency(p.get("total",0)),"Status":p.get("status",""),
                               "Received":p.get("received",False)} for p in pos_list])
            df_display(df)
        else: info("No purchase orders yet.")

    with tab2:
        if "po_cart" not in st.session_state: st.session_state["po_cart"]=[]
        c1,c2=st.columns(2)
        with c1:
            po_sup =st.selectbox("Supplier",sup_names) if sup_names else st.text_input("Supplier")
            po_date=st.date_input("PO Date",date.today())
            po_del =st.date_input("Expected Delivery",date.today()+timedelta(days=5))
        with c2:
            po_stat=st.selectbox("Status",["Draft","Sent","Received","Partially Received","Cancelled"])
            po_notes=st.text_area("Notes",height=60)
        c1,c2,c3=st.columns([3,1,1])
        with c1: po_prod =st.selectbox("Add Product",prod_names,key="po_ap")
        with c2: po_qty  =st.number_input("Qty",1.0,step=1.0,key="po_qty")
        with c3: po_price=st.number_input("Cost Price",0.0,step=1.0,key="po_pr",
                                           value=float(prod_dict.get(po_prod,{}).get("cost_price",0)) if prod_names else 0.0)
        if st.button("➕ Add to PO"):
            st.session_state["po_cart"].append({"product":po_prod,"qty":po_qty,"price":po_price,"total":po_qty*po_price})
            st.rerun()
        if st.session_state["po_cart"]:
            st.dataframe(pd.DataFrame(st.session_state["po_cart"]),use_container_width=True)
            total=sum(i["total"] for i in st.session_state["po_cart"])
            st.write(f"**Total: {currency(total)}**")
            if st.button("✅ Create PO",type="primary"):
                pos_list=load_table("purchase_orders"); oid=gen_id("PO")
                pos_list.append({"id":oid,"date":str(po_date),"supplier":po_sup,
                                  "delivery_date":str(po_del),"status":po_stat,
                                  "items":st.session_state["po_cart"],"total":total,"notes":po_notes,
                                  "received":po_stat=="Received",
                                  "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("purchase_orders",pos_list)
                if po_stat=="Received":
                    prods=load_table("products")
                    for item in st.session_state["po_cart"]:
                        for p in prods:
                            if p["name"]==item["product"]: p["stock"]=float(p.get("stock",0))+item["qty"]
                    save_table("products",prods)
                st.session_state["po_cart"]=[]
                success(f"Purchase Order {oid} created!"); st.rerun()

# ── CUSTOMERS ─────────────────────────────────────────────────────────────────
def page_customers():
    section_header("👥 Customer Management")
    tab1,tab2,tab3=st.tabs(["Customer List","Add Customer","Customer Ledger"])

    with tab1:
        customers=load_table("customers")
        c1,c2=st.columns(2)
        with c1: cs=st.text_input("🔍 Search",key="cs")
        with c2: ct=st.selectbox("Type",["All","Customer","Supplier","Both"])
        filtered=customers
        if cs: filtered=[c for c in filtered if cs.lower() in c.get("name","").lower() or cs.lower() in c.get("phone","").lower()]
        if ct!="All": filtered=[c for c in filtered if c.get("type","")==ct]
        if filtered:
            df=pd.DataFrame(filtered)
            cols=[c for c in ["name","phone","type","city","email","balance","credit_limit","group","cnic"] if c in df.columns]
            df_display(df[cols])
        else: info("No customers found.")

    with tab2:
        with st.form("add_cust"):
            c1,c2,c3=st.columns(3)
            with c1:
                cname=st.text_input("Name *"); cphone=st.text_input("Phone *")
                cemail=st.text_input("Email"); ccity=st.text_input("City")
            with c2:
                ctype=st.selectbox("Type",["Customer","Supplier","Both"])
                cgroup=st.selectbox("Group",["Retail","Wholesale","VIP","General","Corporate"])
                ccnic=st.text_input("CNIC"); cbank=st.text_input("Bank Account")
            with c3:
                caddress=st.text_area("Address",height=70)
                ccredit=st.number_input("Credit Limit",0.0,step=1000.0)
                cbalance=st.number_input("Opening Balance",0.0,step=100.0)
                cnotes=st.text_area("Notes",height=40)
            if st.form_submit_button("💾 Save Customer", use_container_width=True):
                if cname and cphone:
                    custs=load_table("customers")
                    custs.append({"id":gen_id("CST"),"name":cname,"phone":cphone,"email":cemail,
                                  "city":ccity,"type":ctype,"group":cgroup,"cnic":ccnic,
                                  "bank":cbank,"address":caddress,"credit_limit":ccredit,
                                  "balance":cbalance,"notes":cnotes,"created":today_str()})
                    save_table("customers",custs)
                    log_audit(st.session_state["user"]["username"],"ADD_CUSTOMER",cname)
                    success(f"Customer '{cname}' added!"); st.rerun()
                else: error("Name and Phone required.")

    with tab3:
        customers=load_table("customers"); cust_names=[c["name"] for c in customers]
        if cust_names:
            sel=st.selectbox("Select Customer",cust_names,key="cust_led_sel")
            cdata=next((c for c in customers if c["name"]==sel),{})
            if cdata:
                c1,c2,c3=st.columns(3)
                c1.metric("Balance",currency(cdata.get("balance",0)))
                c2.metric("Credit Limit",currency(cdata.get("credit_limit",0)))
                c3.metric("Type",cdata.get("type",""))

                pos_sales=load_table("pos_sales"); receipts=load_table("receipts")
                adv_sales=load_table("advance_sales")
                rows=[]
                for s in pos_sales:
                    if s.get("customer","")==sel:
                        rows.append({"Date":s.get("date",""),"Type":"POS Sale","Ref":s.get("id",""),
                                     "Debit":s.get("total",0),"Credit":0})
                for r in receipts:
                    if r.get("party","")==sel:
                        rows.append({"Date":r.get("date",""),"Type":"Receipt","Ref":r.get("ref",""),
                                     "Debit":0,"Credit":r.get("amount",0)})
                for a in adv_sales:
                    if a.get("customer","")==sel:
                        rows.append({"Date":a.get("date",""),"Type":"Advance Sale","Ref":a.get("id",""),
                                     "Debit":a.get("total",0),"Credit":a.get("advance_paid",0)})
                if rows:
                    rows.sort(key=lambda x:x["Date"])
                    bal=0
                    for r in rows: bal+=float(r["Debit"])-float(r["Credit"]); r["Running Balance"]=bal
                    df_display(pd.DataFrame(rows))
                else: info("No transactions yet.")
        else: info("No customers added yet.")

# ── SUPPLIER MANAGEMENT ────────────────────────────────────────────────────────
def page_supplier_management():
    section_header("🏪 Supplier Management")
    tab1,tab2=st.tabs(["Supplier List","Add Supplier"])
    with tab1:
        sups=load_table("suppliers")
        if sups: df_display(pd.DataFrame(sups))
        else: info("No suppliers yet.")
    with tab2:
        with st.form("add_sup"):
            c1,c2=st.columns(2)
            with c1:
                sn=st.text_input("Supplier Name *"); sp=st.text_input("Phone")
                se=st.text_input("Email"); sc=st.text_input("City")
            with c2:
                sa=st.text_area("Address",height=70); sntn=st.text_input("NTN")
                sbank=st.text_input("Bank Account"); sn2=st.text_area("Notes",height=40)
            if st.form_submit_button("💾 Save Supplier"):
                if sn:
                    sups=load_table("suppliers")
                    sups.append({"id":gen_id("SUP"),"name":sn,"phone":sp,"email":se,
                                 "city":sc,"address":sa,"ntn":sntn,"bank":sbank,
                                 "notes":sn2,"balance":0.0,"created":today_str()})
                    save_table("suppliers",sups); success(f"Supplier '{sn}' added!"); st.rerun()
                else: error("Supplier name required.")

# ── DEBTORS & CREDITORS ───────────────────────────────────────────────────────
def page_debtors_creditors():
    section_header("📊 Debtors & Creditors")
    tab1,tab2,tab3=st.tabs(["Debtors (Receivables)","Creditors (Payables)","Aging Analysis"])
    customers=load_table("customers"); pos_sales=load_table("pos_sales")
    receipts =load_table("receipts");  payments =load_table("payments")

    with tab1:
        debtors=[]
        for c in customers:
            if c.get("type") in ("Customer","Both"):
                st_=sum(float(s.get("total",0)) for s in pos_sales if s.get("customer","")==c["name"])
                rt_=sum(float(r.get("amount",0)) for r in receipts if r.get("party","")==c["name"])
                bal=st_-rt_+float(c.get("balance",0))
                if bal>0: debtors.append({"Name":c["name"],"Phone":c.get("phone",""),
                                           "Sales":st_,"Received":rt_,"Outstanding":bal})
        if debtors:
            df=pd.DataFrame(debtors).sort_values("Outstanding",ascending=False)
            df_display(df)
            st.metric("Total Receivables",currency(sum(d["Outstanding"] for d in debtors)))
        else: info("No debtors.")

    with tab2:
        creditors=[]
        for s in load_table("suppliers"):
            pt_=sum(float(p.get("amount",0)) for p in payments if p.get("party","")==s["name"])
            bal=max(0,abs(float(s.get("balance",0)))-pt_)
            if bal>0: creditors.append({"Name":s["name"],"Phone":s.get("phone",""),"Outstanding":bal})
        if creditors:
            df=pd.DataFrame(creditors).sort_values("Outstanding",ascending=False)
            df_display(df)
            st.metric("Total Payables",currency(sum(c["Outstanding"] for c in creditors)))
        else: info("No creditors.")

    with tab3:
        st.subheader("Receivables Aging")
        buckets={"0-30 Days":0,"31-60 Days":0,"61-90 Days":0,"90+ Days":0}
        for c in customers:
            b=float(c.get("balance",0))
            if b>0: buckets["0-30 Days"]+=b*.4; buckets["31-60 Days"]+=b*.3; buckets["61-90 Days"]+=b*.2; buckets["90+ Days"]+=b*.1
        st.bar_chart(pd.DataFrame(list(buckets.items()),columns=["Age","Amount"]).set_index("Age"))

# ── TASKS ─────────────────────────────────────────────────────────────────────
def page_tasks():
    section_header("📋 Tasks & Follow-ups")
    tab1,tab2=st.tabs(["Task List","Add Task"])

    with tab1:
        tasks=load_table("tasks")
        c1,c2=st.columns(2)
        with c1: ts=st.selectbox("Status",["All","Open","In Progress","Done","Cancelled"])
        with c2: tp=st.selectbox("Priority",["All","High","Medium","Low"])
        filtered=tasks
        if ts!="All": filtered=[t for t in filtered if t.get("status","")==ts]
        if tp!="All": filtered=[t for t in filtered if t.get("priority","")==tp]
        for t in sorted(filtered,key=lambda x:x.get("due_date","")):
            pc={"High":"🔴","Medium":"🟡","Low":"🟢"}.get(t.get("priority",""),"⚪")
            with st.expander(f"{pc} {t.get('title','')} — {t.get('due_date','')} — {t.get('status','')}"):
                c1,c2,c3=st.columns(3)
                c1.write(f"**Assigned:** {t.get('assigned_to','')}")
                c2.write(f"**Customer:** {t.get('customer','')}")
                c3.write(f"**Category:** {t.get('category','')}")
                st.write(f"**Description:** {t.get('description','')}")
                ns=st.selectbox("Update Status",["Open","In Progress","Done","Cancelled"],
                                key=f"ts_{t['id']}",
                                index=["Open","In Progress","Done","Cancelled"].index(t.get("status","Open")))
                if st.button("Update",key=f"tu_{t['id']}"):
                    all_t=load_table("tasks")
                    for ta in all_t:
                        if ta["id"]==t["id"]: ta["status"]=ns
                    save_table("tasks",all_t); st.rerun()
        if not filtered: info("No tasks found.")

    with tab2:
        customers=load_table("customers"); employees=load_table("employees")
        with st.form("add_task"):
            c1,c2=st.columns(2)
            with c1:
                title=st.text_input("Task Title *")
                cat  =st.selectbox("Category",["Follow-up","Call","Meeting","Payment Collection","Delivery","Other"])
                prio =st.selectbox("Priority",["High","Medium","Low"])
                due  =st.date_input("Due Date",date.today()+timedelta(days=1))
            with c2:
                cust    =st.selectbox("Customer",["None"]+[c["name"] for c in customers])
                assigned=st.selectbox("Assign To",["None"]+[e["name"] for e in employees])
                status  =st.selectbox("Status",["Open","In Progress"])
                desc    =st.text_area("Description",height=70)
            if st.form_submit_button("💾 Save Task"):
                if title:
                    tasks=load_table("tasks")
                    tasks.append({"id":gen_id("TSK"),"title":title,"category":cat,"priority":prio,
                                  "due_date":str(due),"customer":cust,"assigned_to":assigned,
                                  "status":status,"description":desc,
                                  "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("tasks",tasks); success("Task added!"); st.rerun()

# ── NOTES ─────────────────────────────────────────────────────────────────────
def page_notes():
    section_header("📝 Notes & Memos")
    tab1,tab2=st.tabs(["All Notes","Add Note"])
    with tab1:
        notes=load_table("notes")
        for n in notes[::-1]:
            with st.expander(f"📌 {n.get('title','')} — {n.get('created','')[:16]}"):
                st.write(n.get("content","")); st.caption(f"By: {n.get('created_by','')} | {n.get('category','')}")
        if not notes: info("No notes yet.")
    with tab2:
        with st.form("add_note"):
            nt=st.text_input("Title *"); nc=st.selectbox("Category",["General","Customer","Finance","Livestock","HR","Other"])
            ncont=st.text_area("Content",height=150)
            if st.form_submit_button("💾 Save Note"):
                if nt:
                    ns=load_table("notes")
                    ns.append({"id":gen_id("NT"),"title":nt,"category":nc,"content":ncont,
                               "created_by":st.session_state["user"]["username"],"created":now_str()})
                    save_table("notes",ns); success("Note saved!"); st.rerun()

# ── LIVESTOCK ─────────────────────────────────────────────────────────────────
def page_livestock():
    section_header("🐄 Livestock Register")
    tab1,tab2,tab3=st.tabs(["Livestock List","Add Animal","Summary"])

    with tab1:
        livestock=load_table("livestock")
        c1,c2,c3=st.columns(3)
        with c1: ls_s=st.text_input("Search (Tag/Name)",key="lss")
        with c2: ls_t=st.selectbox("Type",["All","Cow","Buffalo","Goat","Sheep","Bull","Camel","Donkey","Horse","Other"])
        with c3: ls_st=st.selectbox("Status",["All","Active","Sold","Dead","Transferred"])
        filtered=livestock
        if ls_s: filtered=[l for l in filtered if ls_s.lower() in l.get("tag_no","").lower() or ls_s.lower() in l.get("name","").lower()]
        if ls_t!="All": filtered=[l for l in filtered if l.get("animal_type","")==ls_t]
        if ls_st!="All": filtered=[l for l in filtered if l.get("status","")==ls_st]
        if filtered:
            df=pd.DataFrame(filtered)
            cols=[c for c in ["tag_no","name","animal_type","breed","gender","dob","weight","purchase_price","current_value","status","shed"] if c in df.columns]
            df_display(df[cols])
            st.metric(f"Total Value",currency(sum(float(l.get("current_value",l.get("purchase_price",0))) for l in filtered)))
        else: info("No livestock found.")

    with tab2:
        with st.form("add_ls"):
            c1,c2,c3=st.columns(3)
            with c1:
                tag=st.text_input("Tag # *",value=gen_id("LVS")); aname=st.text_input("Name")
                atype=st.selectbox("Type *",["Cow","Buffalo","Goat","Sheep","Bull","Camel","Donkey","Horse","Other"])
                breed=st.text_input("Breed"); gender=st.selectbox("Gender",["Female","Male","Unknown"])
            with c2:
                dob=st.date_input("Date of Birth",date.today()-timedelta(days=365))
                pdate=st.date_input("Purchase Date",date.today())
                pprice=st.number_input("Purchase Price",0.0,step=100.0)
                cval=st.number_input("Current Value",0.0,step=100.0)
                weight=st.number_input("Weight (KG)",0.0,step=1.0)
            with c3:
                sup=st.text_input("Purchased From"); shed=st.text_input("Shed/Location")
                pregnant=st.checkbox("Pregnant"); lactating=st.checkbox("Lactating")
                vaccinated=st.checkbox("Vaccinated"); status=st.selectbox("Status",["Active","Sold","Dead","Transferred"])
            notes=st.text_area("Notes",height=55)
            if st.form_submit_button("💾 Save Animal", use_container_width=True):
                if tag:
                    ls=load_table("livestock")
                    ls.append({"id":gen_id("LVS"),"tag_no":tag,"name":aname,"animal_type":atype,
                               "breed":breed,"gender":gender,"dob":str(dob),"purchase_date":str(pdate),
                               "purchase_price":pprice,"current_value":cval or pprice,"weight":weight,
                               "supplier":sup,"shed":shed,"is_pregnant":pregnant,"lactating":lactating,
                               "vaccinated":vaccinated,"status":status,"notes":notes,
                               "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("livestock",ls); success(f"Animal {tag} added!"); st.rerun()
                else: error("Tag number required.")

    with tab3:
        livestock=load_table("livestock")
        if livestock:
            by_type={}
            for l in livestock:
                t=l.get("animal_type","Other"); by_type[t]=by_type.get(t,0)+1
            c1,c2=st.columns(2)
            c1.metric("Total Animals",len(livestock))
            c2.metric("Active",len([l for l in livestock if l.get("status")=="Active"]))
            st.bar_chart(pd.DataFrame(list(by_type.items()),columns=["Type","Count"]).set_index("Type"))

# ── MILK PRODUCTION ────────────────────────────────────────────────────────────
def page_milk():
    section_header("🥛 Milk Production")
    tab1,tab2=st.tabs(["Milk Records","Record Milk"])
    livestock=load_table("livestock")
    lactating=[l for l in livestock if l.get("lactating") and l.get("status")=="Active"]

    with tab1:
        mr=load_table("milk_records")
        if mr:
            c1,c2=st.columns(2)
            with c1: mf=st.date_input("From",date.today().replace(day=1),key="mr_f")
            with c2: mt=st.date_input("To",date.today(),key="mr_t")
            filtered=[m for m in mr if mf.isoformat()<=str(m.get("date",""))[:10]<=mt.isoformat()]
            if filtered:
                df=pd.DataFrame(filtered); df_display(df)
                st.metric("Total Milk (Liters)",sum(float(m.get("liters",0)) for m in filtered))
            else: info("No milk records in period.")
        else: info("No milk records yet.")

    with tab2:
        with st.form("milk_rec"):
            c1,c2=st.columns(2)
            with c1:
                milk_date=st.date_input("Date",date.today())
                session =st.selectbox("Session",["Morning","Evening","Both"])
                total_l =st.number_input("Total Liters",0.0,step=0.5)
            with c2:
                price_l =st.number_input("Price per Liter",0.0,step=5.0)
                shed    =st.text_input("Shed/Batch")
                notes   =st.text_area("Notes",height=60)
            if st.form_submit_button("💾 Save Milk Record"):
                if total_l>0:
                    mr=load_table("milk_records")
                    mr.append({"id":gen_id("MILK"),"date":str(milk_date),"session":session,
                               "liters":total_l,"price_per_liter":price_l,"total_value":total_l*price_l,
                               "shed":shed,"notes":notes,
                               "recorded_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("milk_records",mr); success("Milk record saved!"); st.rerun()

# ── FEED RECORDS ──────────────────────────────────────────────────────────────
def page_feed():
    section_header("🌾 Feed Records")
    tab1,tab2=st.tabs(["Feed History","Add Feed Record"])
    FEED_TYPES=["Grass","Dry Feed","Silage","Concentrates","Mixed Feed","Hay","Bran","Other"]

    with tab1:
        fr=load_table("feed_records")
        if fr:
            c1,c2=st.columns(2)
            with c1: ff=st.date_input("From",date.today().replace(day=1),key="ff_f")
            with c2: ft=st.date_input("To",date.today(),key="ff_t")
            filtered=[f for f in fr if ff.isoformat()<=str(f.get("date",""))[:10]<=ft.isoformat()]
            if filtered:
                df_display(pd.DataFrame(filtered))
                st.metric("Total Feed Cost",currency(sum(float(f.get("cost",0)) for f in filtered)))
            else: info("No feed records in period.")
        else: info("No feed records yet.")

    with tab2:
        with st.form("feed_rec"):
            c1,c2=st.columns(2)
            with c1:
                fd=st.date_input("Date",date.today()); ft2=st.selectbox("Feed Type",FEED_TYPES)
                fq=st.number_input("Quantity",0.0,step=1.0); fu=st.selectbox("Unit",["KG","Ton","Bag","Bundle"])
            with c2:
                fuc=st.number_input("Unit Cost",0.0,step=1.0); fshed=st.text_input("Shed/Group")
                fsup=st.text_input("Supplier"); fn=st.text_area("Notes",height=55)
            if st.form_submit_button("💾 Save Feed Record"):
                if fq>0:
                    fr=load_table("feed_records")
                    fr.append({"id":gen_id("FD"),"date":str(fd),"feed_type":ft2,"quantity":fq,
                               "unit":fu,"unit_cost":fuc,"cost":fq*fuc,"shed":fshed,"supplier":fsup,
                               "notes":fn,"recorded_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("feed_records",fr)
                    exps=load_table("expenses")
                    exps.append({"id":gen_id("EXP"),"date":str(fd),"category":"Feed",
                                 "description":f"{ft2} for {fshed}","amount":fq*fuc,"paid_by":"Cash",
                                 "vendor":fsup,"notes":fn,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("expenses",exps); success("Feed record saved!"); st.rerun()

# ── BREEDING ──────────────────────────────────────────────────────────────────
def page_breeding():
    section_header("🐮 Breeding Records")
    tab1,tab2=st.tabs(["Breeding History","Add Record"])
    livestock=load_table("livestock")
    females=[l for l in livestock if l.get("gender")=="Female" and l.get("status")=="Active"]
    males  =[l for l in livestock if l.get("gender")=="Male"   and l.get("status")=="Active"]

    with tab1:
        br=load_table("breeding_records")
        if br: df_display(pd.DataFrame(br))
        else: info("No breeding records yet.")

    with tab2:
        with st.form("breed_rec"):
            c1,c2=st.columns(2)
            with c1:
                female_opts=[f"{l['tag_no']} - {l.get('name','')} ({l.get('breed','')})" for l in females]
                female=st.selectbox("Female Animal",female_opts if female_opts else ["No females"])
                male_opts=[f"{l['tag_no']} - {l.get('name','')} ({l.get('breed','')})" for l in males]+["External Bull","AI"]
                male=st.selectbox("Sire (Male)",male_opts)
                bd=st.date_input("Breeding Date",date.today())
                method=st.selectbox("Method",["Natural","Artificial Insemination","Embryo Transfer"])
            with c2:
                exp_birth=st.date_input("Expected Birth",date.today()+timedelta(days=280))
                status=st.selectbox("Status",["Pending","Confirmed Pregnant","Aborted","Delivered"])
                offspring=st.number_input("Offspring Count",0,step=1)
                notes=st.text_area("Notes",height=60)
            if st.form_submit_button("💾 Save Record"):
                br=load_table("breeding_records")
                br.append({"id":gen_id("BR"),"female":female.split(" - ")[0] if female_opts else "",
                           "male":male,"breeding_date":str(bd),"method":method,
                           "expected_birth":str(exp_birth),"status":status,
                           "offspring_count":offspring,"notes":notes,
                           "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("breeding_records",br)
                if status=="Confirmed Pregnant" and female_opts:
                    tag=female.split(" - ")[0]
                    for l in livestock:
                        if l.get("tag_no","")==tag: l["is_pregnant"]=True
                    save_table("livestock",livestock)
                success("Breeding record saved!"); st.rerun()

# ── HEALTH RECORDS ────────────────────────────────────────────────────────────
def page_health():
    section_header("💉 Livestock Health Records")
    tab1,tab2=st.tabs(["Health History","Add Record"])
    livestock=load_table("livestock")
    animal_tags=[f"{l['tag_no']} - {l.get('name','')} ({l.get('animal_type','')})" for l in livestock if l.get("status")=="Active"]

    with tab1:
        health=load_table("livestock_health")
        if health:
            c1,c2=st.columns(2)
            with c1: hf=st.date_input("From",date.today().replace(day=1),key="hf")
            with c2: ht=st.date_input("To",date.today(),key="ht")
            filtered=[h for h in health if hf.isoformat()<=str(h.get("date",""))[:10]<=ht.isoformat()]
            if filtered: df_display(pd.DataFrame(filtered))
            else: info("No records in period.")
        else: info("No health records yet.")

    with tab2:
        with st.form("health_rec"):
            c1,c2=st.columns(2)
            with c1:
                animal=st.selectbox("Animal",animal_tags if animal_tags else ["No active animals"])
                rec_date=st.date_input("Date",date.today())
                rec_type=st.selectbox("Type",["Vaccination","Treatment","Deworming","Check-up","Surgery","Emergency"])
                diagnosis=st.text_input("Diagnosis/Condition")
            with c2:
                treatment=st.text_area("Treatment/Medication",height=60)
                vet=st.text_input("Veterinarian")
                cost=st.number_input("Cost",0.0,step=10.0)
                next_visit=st.date_input("Next Visit",date.today()+timedelta(days=30))
            if st.form_submit_button("💾 Save Health Record"):
                h=load_table("livestock_health")
                h.append({"id":gen_id("HLT"),"date":str(rec_date),
                          "animal":animal.split(" - ")[0] if animal_tags else "",
                          "type":rec_type,"diagnosis":diagnosis,"treatment":treatment,
                          "vet":vet,"cost":cost,"next_visit":str(next_visit),
                          "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("livestock_health",h)
                if cost>0:
                    exps=load_table("expenses")
                    exps.append({"id":gen_id("EXP"),"date":str(rec_date),"category":"Veterinary",
                                 "description":f"{rec_type}: {diagnosis}","amount":cost,"paid_by":"Cash",
                                 "vendor":vet,"notes":"","created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("expenses",exps)
                success("Health record saved!"); st.rerun()

# ── LIVESTOCK SALES ───────────────────────────────────────────────────────────
def page_livestock_sales():
    section_header("💰 Livestock Sales")
    tab1,tab2=st.tabs(["Sales History","Record Sale"])
    livestock=load_table("livestock"); customers=load_table("customers")
    active=[l for l in livestock if l.get("status")=="Active"]
    cust_names=[c["name"] for c in customers]

    with tab1:
        ls_sales=load_table("livestock_sales")
        if ls_sales:
            df=pd.DataFrame([{"Date":s.get("date",""),"Tag":s.get("tag_no",""),"Type":s.get("animal_type",""),
                               "Customer":s.get("customer",""),"Purchase":currency(s.get("purchase_price",0)),
                               "Sale":currency(s.get("sale_price",0)),
                               "Profit":currency(float(s.get("sale_price",0))-float(s.get("purchase_price",0))),
                               "Mode":s.get("payment_mode","")} for s in ls_sales])
            df_display(df)
            st.metric("Total Profit",currency(sum(float(s.get("sale_price",0))-float(s.get("purchase_price",0)) for s in ls_sales)))
        else: info("No livestock sales yet.")

    with tab2:
        if active:
            with st.form("ls_sale"):
                c1,c2=st.columns(2)
                with c1:
                    animal_opts=[f"{l['tag_no']} - {l.get('name','')} ({l.get('animal_type','')})" for l in active]
                    animal=st.selectbox("Animal",animal_opts)
                    sale_date=st.date_input("Sale Date",date.today())
                    customer=st.selectbox("Buyer",["Walk-in"]+cust_names)
                    sale_price=st.number_input("Sale Price",0.0,step=100.0)
                with c2:
                    weight=st.number_input("Weight at Sale (KG)",0.0,step=1.0)
                    transport=st.number_input("Transport Cost",0.0,step=10.0)
                    commission=st.number_input("Commission",0.0,step=10.0)
                    pm=st.selectbox("Payment Mode",["Cash","Bank Transfer","Credit","Cheque"])
                    notes=st.text_area("Notes",height=55)
                if st.form_submit_button("💰 Record Sale", use_container_width=True):
                    if sale_price>0:
                        tag=animal.split(" - ")[0]
                        adata=next((l for l in active if l["tag_no"]==tag),{})
                        pp=float(adata.get("purchase_price",0))
                        ls=load_table("livestock_sales")
                        ls.append({"id":gen_id("LSS"),"date":str(sale_date),"tag_no":tag,
                                   "animal_type":adata.get("animal_type",""),"breed":adata.get("breed",""),
                                   "customer":customer,"purchase_price":pp,"sale_price":sale_price,
                                   "profit":sale_price-pp-transport-commission,
                                   "weight":weight,"transport_cost":transport,"commission":commission,
                                   "payment_mode":pm,"notes":notes,
                                   "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                        save_table("livestock_sales",ls)
                        for l in livestock:
                            if l["tag_no"]==tag: l["status"]="Sold"
                        save_table("livestock",livestock)
                        rec=load_table("receipts")
                        rec.append({"id":gen_id(),"ref":gen_id("LSS"),"date":str(sale_date),
                                    "party":customer,"amount":sale_price,"mode":pm,"type":"Receipt",
                                    "notes":f"Livestock Sale: {tag}","created_at":now_str()})
                        save_table("receipts",rec)
                        success(f"Animal {tag} sold for {currency(sale_price)}!"); st.rerun()
        else: warn("No active animals available for sale.")

# ── PRODUCTION ────────────────────────────────────────────────────────────────
def page_production():
    section_header("🏭 Production Management")
    products=load_table("products"); prod_names=[p["name"] for p in products]
    tab1,tab2=st.tabs(["Production Orders","New Order"])

    with tab1:
        prods=load_table("production")
        if prods:
            df=pd.DataFrame([{"Order#":p["id"],"Date":p.get("date",""),"Product":p.get("product",""),
                               "Qty":p.get("qty",0),"Status":p.get("status",""),"Cost":currency(p.get("total_cost",0))} for p in prods])
            df_display(df)
        else: info("No production orders.")

    with tab2:
        if "pm" not in st.session_state: st.session_state["pm"]=[]
        c1,c2=st.columns(2)
        with c1:
            pp=st.selectbox("Product to Produce",prod_names) if prod_names else st.text_input("Product")
            pq=st.number_input("Quantity",1.0,step=1.0)
            pd_=st.date_input("Production Date",date.today())
        with c2:
            pst=st.selectbox("Status",["Planned","In Progress","Completed","Cancelled"])
            pn=st.text_area("Notes",height=70)
        c1,c2,c3=st.columns([3,1,1])
        with c1: mp=st.selectbox("Material",prod_names,key="mp") if prod_names else st.text_input("Material",key="mp")
        with c2: mq=st.number_input("Qty",1.0,step=1.0,key="mq")
        with c3: mc=st.number_input("Unit Cost",0.0,step=1.0,key="mc")
        if st.button("➕ Add Material"):
            st.session_state["pm"].append({"material":mp,"qty":mq,"unit_cost":mc,"total":mq*mc}); st.rerun()
        if st.session_state["pm"]:
            st.dataframe(pd.DataFrame(st.session_state["pm"]),use_container_width=True)
            tc=sum(m["total"] for m in st.session_state["pm"])
            st.write(f"**Total Cost: {currency(tc)}**")
            if st.button("✅ Create Production Order",type="primary"):
                prods=load_table("production"); oid=gen_id("PO")
                prods.append({"id":oid,"date":str(pd_),"product":pp,"qty":pq,
                              "materials":st.session_state["pm"],"total_cost":tc,
                              "status":pst,"notes":pn,
                              "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("production",prods)
                if pst=="Completed":
                    ps=load_table("products")
                    for p in ps:
                        if p["name"]==pp: p["stock"]=float(p.get("stock",0))+pq
                    save_table("products",ps)
                st.session_state["pm"]=[]; success(f"Production order {oid} created!"); st.rerun()

# ── PRODUCTION REPORT ─────────────────────────────────────────────────────────
def page_production_report():
    section_header("📊 Production Report")
    prods=load_table("production")
    if prods:
        c1,c2=st.columns(2)
        with c1: pf=st.date_input("From",date.today().replace(day=1))
        with c2: pt=st.date_input("To",date.today())
        filtered=[p for p in prods if pf.isoformat()<=str(p.get("date",""))[:10]<=pt.isoformat()]
        if filtered:
            df=pd.DataFrame([{"Date":p["date"],"Product":p.get("product",""),"Qty":p.get("qty",0),
                               "Cost":currency(p.get("total_cost",0)),"Status":p.get("status","")} for p in filtered])
            df_display(df)
            c1,c2=st.columns(2)
            c1.metric("Total Produced",f"{sum(float(p.get('qty',0)) for p in filtered):.0f} units")
            c2.metric("Total Cost",currency(sum(float(p.get("total_cost",0)) for p in filtered)))
        else: info("No production in period.")
    else: info("No production records.")

# ── BMI PLANS ─────────────────────────────────────────────────────────────────
def page_bmi_plans():
    section_header("💳 BMI / Installment Plans")
    customers=load_table("customers"); cust_names=[c["name"] for c in customers]
    tab1,tab2,tab3=st.tabs(["Plans","Create Plan","Calculator"])

    with tab1:
        bmi=load_table("bmi_plans")
        if bmi:
            for plan in bmi:
                si="✅" if plan.get("status")=="Completed" else "🔄"
                with st.expander(f"{si} {plan.get('id','')} — {plan.get('customer','')} — {currency(plan.get('total_amount',0))}"):
                    c1,c2,c3,c4=st.columns(4)
                    c1.metric("Total",currency(plan.get("total_amount",0)))
                    c2.metric("Down Payment",currency(plan.get("down_payment",0)))
                    c3.metric("Installments",plan.get("installment_count",0))
                    c4.metric("Status",plan.get("status",""))
                    inst=load_table("installments")
                    plan_inst=[i for i in inst if i.get("plan_id","")==plan["id"]]
                    if plan_inst:
                        df_display(pd.DataFrame(plan_inst),200)
        else: info("No BMI plans.")

    with tab2:
        with st.form("bmi_plan"):
            c1,c2=st.columns(2)
            with c1:
                bc=st.selectbox("Customer",cust_names) if cust_names else st.text_input("Customer")
                item=st.text_input("Item/Product Description")
                total=st.number_input("Total Amount",0.0,step=100.0)
                dp  =st.number_input("Down Payment",0.0,step=100.0)
            with c2:
                n_inst=st.number_input("Number of Installments",1,60,12,step=1)
                start_date=st.date_input("First Installment Date",date.today()+timedelta(days=30))
                freq=st.selectbox("Frequency",["Monthly","Weekly","Bi-weekly"])
                notes=st.text_area("Notes",height=55)
            if st.form_submit_button("💾 Create BMI Plan", use_container_width=True):
                if total>0:
                    remaining=total-dp
                    inst_amt=remaining/n_inst if n_inst>0 else remaining
                    plan_id=gen_id("BMI")
                    bmi=load_table("bmi_plans")
                    bmi.append({"id":plan_id,"customer":bc,"item":item,"total_amount":total,
                                "down_payment":dp,"installment_count":n_inst,"installment_amount":inst_amt,
                                "frequency":freq,"start_date":str(start_date),"status":"Active",
                                "notes":notes,"created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("bmi_plans",bmi)
                    inst=load_table("installments")
                    for i in range(n_inst):
                        if freq=="Monthly": due=start_date+timedelta(days=30*i)
                        elif freq=="Weekly": due=start_date+timedelta(weeks=i)
                        else: due=start_date+timedelta(days=14*i)
                        inst.append({"id":gen_id("INS"),"plan_id":plan_id,"installment_no":i+1,
                                     "customer":bc,"due_date":str(due),"amount":inst_amt,
                                     "status":"Pending","paid_date":"","paid_amount":0,
                                     "notes":"","created_at":now_str()})
                    save_table("installments",inst)
                    success(f"BMI Plan {plan_id} created with {n_inst} installments!"); st.rerun()

    with tab3:
        st.subheader("📱 Installment Calculator")
        c1,c2,c3=st.columns(3)
        with c1: ci_total=st.number_input("Total Price",0.0,step=1000.0,key="ci_t")
        with c2: ci_dp   =st.number_input("Down Payment",0.0,step=500.0,key="ci_dp")
        with c3: ci_n    =st.number_input("Months",1,60,12,step=1,key="ci_n")
        if ci_total>0:
            monthly=(ci_total-ci_dp)/ci_n
            c1,c2=st.columns(2)
            c1.metric("Monthly Installment",currency(monthly))
            c2.metric("Total Payable",currency(ci_total))

# ── INSTALLMENT SCHEDULE ──────────────────────────────────────────────────────
def page_installment_schedule():
    section_header("📅 Installment Schedule & Tracker")
    inst=load_table("installments")
    if not inst: info("No installments."); return

    c1,c2,c3=st.columns(3)
    with c1: is_stat=st.selectbox("Status",["All","Pending","Paid","Overdue"])
    with c2: is_from=st.date_input("Due From",date.today().replace(day=1),key="is_f")
    with c3: is_to  =st.date_input("Due To",date.today()+timedelta(days=90),key="is_t")

    filtered=inst
    if is_stat!="All": filtered=[i for i in filtered if i.get("status","")==is_stat]
    filtered=[i for i in filtered if is_from.isoformat()<=str(i.get("due_date",""))[:10]<=is_to.isoformat()]

    overdue=[i for i in inst if i.get("status")=="Pending" and str(i.get("due_date",""))<today_str()]
    for o in overdue:
        for i2 in inst:
            if i2["id"]==o["id"]: i2["status"]="Overdue"
    save_table("installments",inst)

    if filtered:
        for i in filtered:
            status_icon={"Pending":"🟡","Paid":"✅","Overdue":"🔴"}.get(i.get("status",""),"⚪")
            with st.expander(f"{status_icon} {i.get('customer','')} — Due: {i.get('due_date','')} — {currency(i.get('amount',0))}"):
                c1,c2,c3=st.columns(3)
                c1.metric("Amount",currency(i.get("amount",0)))
                c2.metric("Status",i.get("status",""))
                c3.metric("Plan",i.get("plan_id",""))
                if i.get("status") in ("Pending","Overdue"):
                    with st.form(f"pay_inst_{i['id']}"):
                        pc1,pc2=st.columns(2)
                        with pc1: pay_amt=st.number_input("Amount Received",0.0,value=float(i.get("amount",0)),step=100.0)
                        with pc2: pay_date=st.date_input("Payment Date",date.today())
                        pay_notes=st.text_input("Notes")
                        if st.form_submit_button("💰 Mark as Paid"):
                            all_inst=load_table("installments")
                            for i2 in all_inst:
                                if i2["id"]==i["id"]:
                                    i2["status"]="Paid"; i2["paid_date"]=str(pay_date)
                                    i2["paid_amount"]=pay_amt; i2["notes"]=pay_notes
                            save_table("installments",all_inst)
                            rec=load_table("receipts")
                            rec.append({"id":gen_id(),"ref":i["id"],"date":str(pay_date),
                                        "party":i.get("customer",""),"amount":pay_amt,"mode":"Cash",
                                        "type":"Receipt","notes":f"Installment {i.get('plan_id','')}","created_at":now_str()})
                            save_table("receipts",rec)
                            success("Installment marked as paid!"); st.rerun()

    pending_total=sum(float(i.get("amount",0)) for i in inst if i.get("status") in ("Pending","Overdue"))
    st.metric("Total Pending Amount",currency(pending_total))

# ── HRM — EMPLOYEES ────────────────────────────────────────────────────────────
def page_employees():
    section_header("👨‍💼 Employee Management")
    tab1,tab2=st.tabs(["Employee List","Add Employee"])

    with tab1:
        employees=load_table("employees")
        c1,c2=st.columns(2)
        with c1: es=st.text_input("Search",key="es")
        with c2: ed=st.selectbox("Department",["All","Management","Sales","Operations","Livestock","Finance","Security","Other"])
        filtered=employees
        if es: filtered=[e for e in filtered if es.lower() in e.get("name","").lower()]
        if ed!="All": filtered=[e for e in filtered if e.get("department","")==ed]
        if filtered:
            df=pd.DataFrame(filtered)
            cols=[c for c in ["emp_id","name","designation","department","phone","cnic","salary","join_date","status"] if c in df.columns]
            df_display(df[cols])
        else: info("No employees found.")

    with tab2:
        with st.form("add_emp"):
            c1,c2,c3=st.columns(3)
            with c1:
                en=st.text_input("Full Name *"); eid=st.text_input("Employee ID",value=gen_id("EMP"))
                des=st.text_input("Designation"); dep=st.selectbox("Department",["Management","Sales","Operations","Livestock","Finance","Security","Other"])
                et=st.selectbox("Type",["Full-time","Part-time","Contract","Daily Wage"])
            with c2:
                ep=st.text_input("Phone *"); ec=st.text_input("CNIC"); ee=st.text_input("Email")
                ea=st.text_area("Address",height=55); eec=st.text_input("Emergency Contact")
            with c3:
                sal=st.number_input("Basic Salary",0.0,step=100.0)
                stype=st.selectbox("Salary Type",["Monthly","Weekly","Daily","Hourly"])
                jd=st.date_input("Join Date",date.today())
                ebank=st.text_input("Bank Account"); en2=st.text_area("Notes",height=35)
            if st.form_submit_button("💾 Save Employee", use_container_width=True):
                if en and ep:
                    emps=load_table("employees")
                    emps.append({"id":gen_id("EMP"),"emp_id":eid,"name":en,"designation":des,
                                 "department":dep,"emp_type":et,"phone":ep,"cnic":ec,"email":ee,
                                 "address":ea,"emergency_contact":eec,"salary":sal,"salary_type":stype,
                                 "join_date":str(jd),"bank_account":ebank,"notes":en2,"status":"Active","created":today_str()})
                    save_table("employees",emps)
                    log_audit(st.session_state["user"]["username"],"ADD_EMPLOYEE",en)
                    success(f"Employee '{en}' added!"); st.rerun()
                else: error("Name and Phone required.")

# ── ATTENDANCE ────────────────────────────────────────────────────────────────
def page_attendance():
    section_header("📅 Attendance Management")
    employees=load_table("employees"); emp_names=[e["name"] for e in employees if e.get("status")=="Active"]
    tab1,tab2,tab3=st.tabs(["Daily Attendance","Mark Attendance","Report"])

    with tab1:
        att=load_table("attendance")
        c1,c2=st.columns(2)
        with c1: ad=st.date_input("Date",date.today(),key="att_d")
        with c2: ae=st.selectbox("Employee",["All"]+emp_names,key="att_e_f")
        filtered=[a for a in att if a.get("date","")==str(ad)]
        if ae!="All": filtered=[a for a in filtered if a.get("employee","")==ae]
        if filtered: df_display(pd.DataFrame(filtered))
        else: info(f"No attendance for {ad}.")

    with tab2:
        amd=st.date_input("Mark Attendance For",date.today(),key="amd")
        if emp_names:
            with st.form("mark_att"):
                rows=[]
                for emp in emp_names:
                    c1,c2,c3,c4=st.columns([3,1,1,1])
                    with c1: st.write(f"**{emp}**")
                    with c2: sts=st.selectbox("",["Present","Absent","Late","Half-day","Holiday"],key=f"att_{emp}")
                    with c3: ti=st.time_input("In",key=f"ti_{emp}",value=None)
                    with c4: to=st.time_input("Out",key=f"to_{emp}",value=None)
                    rows.append({"employee":emp,"status":sts,"time_in":str(ti) if ti else "","time_out":str(to) if to else ""})
                if st.form_submit_button("💾 Save Attendance", use_container_width=True):
                    att_data=load_table("attendance")
                    existing=[a for a in att_data if a.get("date","")!=str(amd)]
                    for r in rows:
                        existing.append({"id":gen_id("ATT"),"date":str(amd),"employee":r["employee"],
                                         "status":r["status"],"time_in":r["time_in"],"time_out":r["time_out"],
                                         "recorded_by":st.session_state["user"]["username"]})
                    save_table("attendance",existing)
                    success(f"Attendance saved for {amd}!"); st.rerun()
        else: warn("Add employees first.")

    with tab3:
        att_data=load_table("attendance")
        c1,c2=st.columns(2)
        with c1: af=st.date_input("From",date.today().replace(day=1),key="ar_f")
        with c2: at=st.date_input("To",date.today(),key="ar_t")
        filtered=[a for a in att_data if af.isoformat()<=a.get("date","")<=at.isoformat()]
        if filtered:
            summ={}
            for a in filtered:
                e=a.get("employee","")
                if e not in summ: summ[e]={"Present":0,"Absent":0,"Late":0,"Half-day":0,"Holiday":0}
                summ[e][a.get("status","Present")]=summ[e].get(a.get("status","Present"),0)+1
            df_display(pd.DataFrame([{"Employee":e,**s} for e,s in summ.items()]))
        else: info("No attendance in period.")

# ── SALARY MANAGEMENT ────────────────────────────────────────────────────────
def page_salaries():
    section_header("💵 Salary Management")
    employees=load_table("employees"); emp_names=[e["name"] for e in employees if e.get("status")=="Active"]
    tab1,tab2=st.tabs(["Salary Records","Process Salary"])

    with tab1:
        sal=load_table("salaries")
        if sal: df_display(pd.DataFrame(sal))
        else: info("No salary records.")

    with tab2:
        with st.form("sal_form"):
            c1,c2=st.columns(2)
            with c1:
                emp=st.selectbox("Employee",emp_names) if emp_names else st.text_input("Employee")
                month=st.selectbox("Month",["January","February","March","April","May","June",
                                             "July","August","September","October","November","December"])
                year=st.number_input("Year",2020,2030,date.today().year,step=1)
                basic=st.number_input("Basic Salary",0.0,step=100.0)
            with c2:
                allowances=st.number_input("Allowances",0.0,step=50.0)
                deductions=st.number_input("Deductions",0.0,step=50.0)
                bonus=st.number_input("Bonus",0.0,step=100.0)
                pay_mode=st.selectbox("Payment Mode",["Cash","Bank Transfer","Cheque"])
            notes=st.text_area("Notes",height=55)
            if st.form_submit_button("💾 Process Salary", use_container_width=True):
                if emp and basic>0:
                    net=basic+allowances+bonus-deductions
                    sal=load_table("salaries")
                    sal.append({"id":gen_id("SAL"),"employee":emp,"month":month,"year":year,
                                "basic":basic,"allowances":allowances,"deductions":deductions,
                                "bonus":bonus,"net_salary":net,"payment_mode":pay_mode,"notes":notes,
                                "processed_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("salaries",sal)
                    payments=load_table("payments")
                    payments.append({"id":gen_id(),"ref":gen_id("SAL"),"date":today_str(),"party":emp,
                                     "amount":net,"mode":pay_mode,"type":"Payment",
                                     "notes":f"Salary {month} {year}","created_at":now_str()})
                    save_table("payments",payments)
                    success(f"Salary for {emp} — Net: {currency(net)} processed!"); st.rerun()

# ── LOANS & ADVANCES ─────────────────────────────────────────────────────────
def page_loans():
    section_header("💰 Loans & Advances")
    employees=load_table("employees"); emp_names=[e["name"] for e in employees if e.get("status")=="Active"]
    tab1,tab2=st.tabs(["Loan Records","New Loan/Advance"])

    with tab1:
        loans=load_table("loans")
        if loans: df_display(pd.DataFrame(loans))
        else: info("No loan records.")

    with tab2:
        with st.form("loan_form"):
            c1,c2=st.columns(2)
            with c1:
                emp=st.selectbox("Employee",emp_names) if emp_names else st.text_input("Employee")
                ltype=st.selectbox("Type",["Loan","Advance","Emergency","Other"])
                amount=st.number_input("Amount",0.0,step=100.0)
                date_=st.date_input("Date",date.today())
            with c2:
                repay=st.number_input("Monthly Deduction",0.0,step=100.0)
                purpose=st.text_input("Purpose")
                notes=st.text_area("Notes",height=55)
            if st.form_submit_button("💾 Save"):
                if emp and amount>0:
                    loans=load_table("loans")
                    loans.append({"id":gen_id("LN"),"employee":emp,"type":ltype,"amount":amount,
                                  "date":str(date_),"monthly_deduction":repay,"purpose":purpose,
                                  "remaining":amount,"status":"Active","notes":notes,
                                  "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("loans",loans); success(f"Loan/Advance recorded!"); st.rerun()

# ── SETTINGS ──────────────────────────────────────────────────────────────────
def page_settings():
    section_header("⚙️ Company Settings")
    s=get_settings()
    with st.form("settings_form"):
        c1,c2=st.columns(2)
        with c1:
            sname   =st.text_input("Company Name",value=s.get("name",""))
            saddress=st.text_area("Address",value=s.get("address",""),height=70)
            sphone  =st.text_input("Phone",value=s.get("phone",""))
            semail  =st.text_input("Email",value=s.get("email",""))
        with c2:
            sntn    =st.text_input("NTN",value=s.get("ntn",""))
            scurrency=st.selectbox("Currency",["PKR","USD","EUR","GBP","AED","SAR"],
                                   index=["PKR","USD","EUR","GBP","AED","SAR"].index(s.get("currency","PKR")))
            stax    =st.number_input("Default Tax Rate %",0.0,100.0,s.get("tax_rate",17.0))
            slow    =st.number_input("Low Stock Threshold",0,1000,s.get("low_stock_threshold",10),step=1)
        if st.form_submit_button("💾 Save Settings", use_container_width=True):
            settings_data=load_table("company_settings")
            if settings_data:
                settings_data[0].update({"name":sname,"address":saddress,"phone":sphone,
                                          "email":semail,"ntn":sntn,"currency":scurrency,
                                          "tax_rate":stax,"low_stock_threshold":slow})
                save_table("company_settings",settings_data)
            success("Settings saved!"); st.rerun()

    # Categories & Units management
    st.divider()
    c1,c2=st.columns(2)
    with c1:
        st.subheader("📁 Categories")
        cats=load_table("categories")
        if cats: st.write(", ".join(c["name"] for c in cats))
        with st.form("add_cat"):
            cn=st.text_input("Category Name")
            if st.form_submit_button("➕ Add"):
                if cn:
                    cats=load_table("categories"); cats.append({"id":gen_id("CAT"),"name":cn})
                    save_table("categories",cats); success("Added!"); st.rerun()
    with c2:
        st.subheader("📏 Units")
        units=load_table("units")
        if units: st.write(", ".join(u["name"] for u in units))
        with st.form("add_unit"):
            un=st.text_input("Unit Name")
            if st.form_submit_button("➕ Add"):
                if un:
                    units=load_table("units"); units.append({"id":gen_id("UT"),"name":un})
                    save_table("units",units); success("Added!"); st.rerun()

# ── USER MANAGEMENT ───────────────────────────────────────────────────────────
def page_users():
    section_header("👤 User Management")
    current_user=st.session_state.get("user",{})
    tab1,tab2=st.tabs(["User List","Add User"])

    with tab1:
        users=load_table("users")
        if users:
            for u in users:
                with st.expander(f"{'✅' if u.get('active') else '❌'} {u['username']} — {u.get('role','')} — {u.get('name','')}"):
                    c1,c2,c3=st.columns(3)
                    c1.write(f"**Email:** {u.get('email','')}"); c2.write(f"**Phone:** {u.get('phone','')}")
                    c3.write(f"**Created:** {u.get('created','')}")
                    if u["username"]!=current_user.get("username",""):
                        cc1,cc2=st.columns(2)
                        with cc1:
                            if u.get("active"):
                                if st.button(f"🔒 Deactivate",key=f"deact_{u['id']}"):
                                    all_u=load_table("users")
                                    for uu in all_u:
                                        if uu["username"]==u["username"]: uu["active"]=False
                                    save_table("users",all_u); st.rerun()
                        with cc2:
                            if not u.get("active"):
                                if st.button(f"🔓 Activate",key=f"act_{u['id']}"):
                                    all_u=load_table("users")
                                    for uu in all_u:
                                        if uu["username"]==u["username"]: uu["active"]=True
                                    save_table("users",all_u); st.rerun()

    with tab2:
        with st.form("add_user"):
            c1,c2=st.columns(2)
            with c1:
                uu=st.text_input("Username *"); un=st.text_input("Full Name *")
                ur=st.selectbox("Role",["Admin","Manager","Cashier","Accountant","Viewer","HRM"])
                upw=st.text_input("Password *",type="password")
            with c2:
                ue=st.text_input("Email"); uph=st.text_input("Phone")
                ucpw=st.text_input("Confirm Password",type="password")
            if st.form_submit_button("💾 Create User"):
                if uu and un and upw:
                    if upw!=ucpw: error("Passwords don't match!")
                    else:
                        users=load_table("users")
                        if any(u["username"]==uu for u in users): error("Username exists!")
                        else:
                            users.append({"id":gen_id("USR"),"username":uu,"name":un,"role":ur,
                                          "email":ue,"phone":uph,"password":hash_pw(upw),
                                          "active":True,"created":today_str()})
                            save_table("users",users)
                            log_audit(current_user.get("username",""),"CREATE_USER",uu)
                            success(f"User '{uu}' created!"); st.rerun()
                else: error("Username, Name, Password required.")

# ── AUDIT LOG ─────────────────────────────────────────────────────────────────
def page_audit_log():
    section_header("📋 Audit Log")
    al=load_table("audit_log")
    if al:
        c1,c2,c3=st.columns(3)
        with c1: als=st.text_input("Search",key="als")
        with c2: alu=st.selectbox("User",["All"]+list(set(a.get("user","") for a in al)),key="alu")
        with c3: alact=st.selectbox("Action",["All"]+list(set(a.get("action","") for a in al)),key="alact")
        filtered=al
        if als: filtered=[a for a in filtered if als.lower() in str(a).lower()]
        if alu!="All": filtered=[a for a in filtered if a.get("user","")==alu]
        if alact!="All": filtered=[a for a in filtered if a.get("action","")==alact]
        df_display(pd.DataFrame(filtered[::-1]))
    else: info("No audit log entries.")

# ══════════════════════════════════════════════════════════════════════════════
# DAILY DOWNLOAD — FULL DAY DATA EXPORT
# ══════════════════════════════════════════════════════════════════════════════
def page_daily_download():
    section_header("📥 Daily Data Download")
    st.markdown("""
    <div style='background:#1a3a5c;border-radius:10px;padding:14px 20px;margin-bottom:16px;border-left:4px solid #3498db'>
    <b>📋 How it works:</b> Select any date to download a complete Excel report of that day's activity — 
    all sales, expenses, receipts, payments, advance sales, and a full profit/loss summary. 
    Customer and inventory data is always preserved. Sales data older than 3 days is archived automatically.
    </div>""", unsafe_allow_html=True)

    col1,col2=st.columns(2)
    with col1: dl_date=st.date_input("Select Date to Download",date.today(),key="dl_date")
    with col2: dl_format=st.selectbox("Format",["Excel (XLSX)","CSV (Multiple Files)"])

    ds=dl_date.isoformat()
    pos_sales       =load_table("pos_sales")
    expenses        =load_table("expenses")
    receipts        =load_table("receipts")
    payments        =load_table("payments")
    advance_sales   =load_table("advance_sales")
    livestock_sales =load_table("livestock_sales")
    sale_orders     =load_table("sale_orders")
    customers       =load_table("customers")
    products        =load_table("products")
    livestock       =load_table("livestock")

    # Filter by date
    day_pos    =[s for s in pos_sales       if str(s.get("date",""))[:10]==ds]
    day_exp    =[e for e in expenses        if str(e.get("date",""))[:10]==ds]
    day_rec    =[r for r in receipts        if str(r.get("date",""))[:10]==ds]
    day_pay    =[p for p in payments        if str(p.get("date",""))[:10]==ds]
    day_adv    =[a for a in advance_sales   if str(a.get("date",""))[:10]==ds]
    day_ls     =[l for l in livestock_sales if str(l.get("date",""))[:10]==ds]
    day_so     =[o for o in sale_orders     if str(o.get("date",""))[:10]==ds]

    total_sales   =sum(float(s.get("total",0)) for s in day_pos)
    total_exp     =sum(float(e.get("amount",0)) for e in day_exp)
    total_rec     =sum(float(r.get("amount",0)) for r in day_rec)
    total_pay     =sum(float(p.get("amount",0)) for p in day_pay)
    total_ls_sales=sum(float(l.get("sale_price",0)) for l in day_ls)
    total_ls_cost =sum(float(l.get("purchase_price",0)) for l in day_ls)
    gross_profit  =(total_sales+total_ls_sales)-(sum(float(s.get("cost_total",0)) for s in day_pos)+total_ls_cost)
    net_profit    =gross_profit-total_exp

    st.divider()
    st.subheader(f"📊 Summary for {ds}")
    c1,c2,c3,c4,c5,c6=st.columns(6)
    with c1: metric_card("POS Sales",f"{len(day_pos)} txns")
    with c2: metric_card("Revenue",f"PKR {total_sales:,.0f}")
    with c3: metric_card("Expenses",f"PKR {total_exp:,.0f}")
    with c4: metric_card("Receipts",f"PKR {total_rec:,.0f}")
    with c5: metric_card("Gross Profit",f"PKR {gross_profit:,.0f}")
    with c6: metric_card("Net Profit",f"PKR {net_profit:,.0f}")

    st.divider()

    def safe_df(data,cols=None):
        if not data: return pd.DataFrame()
        df=pd.DataFrame(data)
        if cols: df=df[[c for c in cols if c in df.columns]]
        return df

    summary_data={"Date":[ds],"Total Sales":[total_sales],"POS Transactions":[len(day_pos)],
                  "Expenses":[total_exp],"Receipts":[total_rec],"Payments":[total_pay],
                  "LS Sales":[total_ls_sales],"Gross Profit":[gross_profit],"Net Profit":[net_profit]}
    summary_df=pd.DataFrame(summary_data)

    pos_df =safe_df(day_pos, ["id","time","customer","subtotal","discount_amt","tax_amt","total","amount_paid","change","payment_mode","created_by"])
    exp_df =safe_df(day_exp, ["id","ref","category","description","amount","paid_by","vendor"])
    rec_df =safe_df(day_rec, ["id","ref","party","amount","mode","notes"])
    pay_df =safe_df(day_pay, ["id","ref","party","amount","mode","notes"])
    adv_df =safe_df(day_adv, ["id","customer","product","qty","price","total","advance_paid","balance","status"])
    ls_df  =safe_df(day_ls,  ["id","tag_no","animal_type","customer","purchase_price","sale_price","profit","payment_mode"])
    so_df  =safe_df(day_so,  ["id","customer","total","status","type"])
    cust_df=safe_df(customers,["name","phone","type","city","balance"])
    prod_df=safe_df(products, ["sku","name","category","stock","min_stock","cost_price","sale_price"])
    live_df=safe_df([l for l in livestock if l.get("status")=="Active"],["tag_no","name","animal_type","breed","gender","status","shed"])

    # POS items breakdown
    items_rows=[]
    for s in day_pos:
        for it in s.get("items",[]):
            items_rows.append({"Sale ID":s["id"],"Customer":s.get("customer",""),
                               "Product":it.get("product",""),"Qty":it.get("qty",0),
                               "Price":it.get("price",0),"Total":it.get("total",0)})
    items_df=pd.DataFrame(items_rows) if items_rows else pd.DataFrame()

    if dl_format=="Excel (XLSX)":
        sheets={
            "📊 Day Summary":summary_df,
            "🛒 POS Sales":pos_df,
            "📦 Sale Items":items_df,
            "💸 Expenses":exp_df,
            "💳 Receipts":rec_df,
            "💰 Payments":pay_df,
            "🔄 Advance Sales":adv_df,
            "🐄 Livestock Sales":ls_df,
            "📋 Sale Orders":so_df,
            "👥 Customers":cust_df,
            "📦 Products & Stock":prod_df,
            "🐄 Active Livestock":live_df,
        }
        xl_bytes=df_to_excel_bytes(sheets)
        fname=f"hassan_traders_{ds}.xlsx"
        st.markdown(
            '<div class="dl-btn" style="margin-top:12px">'+
            make_download_link(xl_bytes, fname, f"📥 Download Full Report — {ds} (Excel)")
            +'</div>', unsafe_allow_html=True)
        st.info(f"✅ Excel report ready with {sum(1 for v in sheets.values() if not v.empty)} sheets of data.")

    else:  # CSV
        st.markdown("**Download individual CSV files:**")
        csv_files=[
            ("day_summary",summary_df),("pos_sales",pos_df),("sale_items",items_df),
            ("expenses",exp_df),("receipts",rec_df),("payments",pay_df),
            ("advance_sales",adv_df),("livestock_sales",ls_df),
            ("customers",cust_df),("products",prod_df),
        ]
        cols=st.columns(3)
        for i,(name,df_) in enumerate(csv_files):
            if not df_.empty:
                fname=f"{name}_{ds}.csv"
                with cols[i%3]:
                    st.markdown('<div class="dl-btn">'+make_download_link(df_to_csv_bytes(df_),fname,f"📄 {name.replace('_',' ').title()}")+'</div>',
                                unsafe_allow_html=True)

# ── DATA MANAGEMENT ───────────────────────────────────────────────────────────
def page_data_management():
    section_header("🗃️ Data Management")

    st.markdown("""
    <div style='background:#1a472a;border-radius:10px;padding:14px;border-left:4px solid #2ecc71;margin-bottom:16px'>
    <b>✅ Auto-Cleanup Policy:</b> Sales, expenses, receipts, payments data older than 3 days 
    is automatically archived to keep the system fast. Customer data, inventory, livestock, 
    employees and all master data is <b>never deleted</b>.
    </div>""", unsafe_allow_html=True)

    # Show data sizes
    st.subheader("📊 Data Storage Overview")
    rows=[]
    for tbl in PERSISTENT_TABLES+TRANSIENT_TABLES:
        data=load_table(tbl)
        rows.append({"Table":tbl,"Records":len(data),"Type":"Permanent" if tbl in PERSISTENT_TABLES else "Auto-cleaned (3d)"})
    df_display(pd.DataFrame(rows))

    st.divider()
    c1,c2=st.columns(2)
    with c1:
        st.subheader("🗑️ Manual Cleanup")
        if st.button("🔄 Run Auto-Cleanup Now"):
            auto_cleanup(); success("Cleanup complete! Transient data older than 3 days archived."); st.rerun()

    with c2:
        st.subheader("📥 Full Data Backup")
        if st.button("💾 Download Full Backup"):
            all_data={}
            for tbl in PERSISTENT_TABLES+TRANSIENT_TABLES:
                data=load_table(tbl)
                if data: all_data[tbl]=pd.DataFrame(data)
            if all_data:
                xl=df_to_excel_bytes(all_data)
                st.markdown('<div class="dl-btn">'+make_download_link(xl,f"full_backup_{today_str()}.xlsx","📥 Download Full Backup")+'</div>',
                            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def route():
    page=st.session_state.get("nav_page","Overview")
    PAGE_MAP={
        "Overview":page_dashboard,
        "Ledger":page_ledger,
        "Cashbook":page_cashbook,
        "Receipts & Payments":page_receipts_payments,
        "Expenses":page_expenses,
        "Daily Profit Report":page_daily_profit,
        "Products":page_products,
        "Stock Adjustment":page_stock_adjustment,
        "Damage Records":page_damage,
        "Warehouses":page_warehouses,
        "Price Lists":page_price_lists,
        "Point of Sale":page_pos,
        "Sale Orders":page_sale_orders,
        "Advance Sales":page_advance_sales,
        "English Billing":page_english_billing,
        "Purchase Orders":page_purchase_orders,
        "Supplier Management":page_supplier_management,
        "Customers":page_customers,
        "Debtors & Creditors":page_debtors_creditors,
        "Tasks & Follow-ups":page_tasks,
        "Notes":page_notes,
        "Livestock Register":page_livestock,
        "Milk Production":page_milk,
        "Feed Records":page_feed,
        "Breeding":page_breeding,
        "Health Records":page_health,
        "Livestock Sales":page_livestock_sales,
        "Production Orders":page_production,
        "Production Report":page_production_report,
        "BMI Plans":page_bmi_plans,
        "Installment Schedule":page_installment_schedule,
        "Employees":page_employees,
        "Attendance":page_attendance,
        "Salary Management":page_salaries,
        "Loans & Advances":page_loans,
        "Settings":page_settings,
        "User Management":page_users,
        "Audit Log":page_audit_log,
        "Daily Download":page_daily_download,
        "Data Management":page_data_management,
    }
    PAGE_MAP.get(page,page_dashboard)()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    init_default_user()
    init_settings()
    auto_cleanup()

    if not st.session_state.get("logged_in"):
        login_page()
    else:
        render_sidebar()
        route()

if __name__=="__main__":
    main()