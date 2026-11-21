
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# ==========================================
# تنظیمات اصلی برنامه
# ==========================================

st.set_page_config(
    page_title="دستیار هوشمند تولید محتوا",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

HISTORY_FILE = Path(__file__).resolve().parent / "history.json"

CONTENT_TYPES = [
    "سناریوی ریلز",
    "کپشن اینستاگرام",
    "ایده تولید محتوا",
    "متن تبلیغاتی",
    "محتوای آموزشی"
]

PLATFORMS = [
    "اینستاگرام",
    "تلگرام",
    "وب‌سایت",
    "لینکدین"
]

TONES = [
    "صمیمی و دوستانه",
    "رسمی و حرفه‌ای",
    "آموزشی",
    "خلاقانه و جذاب"
]


# ==========================================
# مدیریت تاریخچه
# ==========================================

def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(
            HISTORY_FILE.read_text(encoding="utf-8")
        )

        if not isinstance(data, list):
            return []

        # سازگاری با تاریخچه‌های قبلی
        changed = False

        for item in data:
            if not isinstance(item, dict):
                continue

            if not item.get("id"):
                item["id"] = str(uuid4())
                changed = True

        if changed:
            save_history(data)

        return [item for item in data if isinstance(item, dict)]

    except (json.JSONDecodeError, OSError):
        st.error(
            "خواندن فایل تاریخچه با مشکل مواجه شد. "
            "فایل history.json را بررسی کن."
        )
        return []


def save_history(history):
    try:
        temp_file = HISTORY_FILE.with_suffix(".tmp")

        temp_file.write_text(
            json.dumps(
                history,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

        temp_file.replace(HISTORY_FILE)
        return True

    except OSError as error:
        st.error(f"ذخیره تاریخچه انجام نشد: {error}")
        return False


def find_item(history, item_id):
    for item in history:
        if str(item.get("id")) == str(item_id):
            return item
    return None


# ==========================================
# طراحی ظاهری
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Vazirmatn', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #faf8ff, #f2edff);
    color: #30264b;
    direction: rtl;
}

.block-container {
    max-width: 1100px;
    padding: 2rem 1.5rem 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    background: linear-gradient(120deg, #7954c8, #a58ade, #c2a9ec);
    border-radius: 25px;
    padding: 38px 25px;
    text-align: center;
    color: white;
    box-shadow: 0 12px 30px #9875d533;
    margin-bottom: 30px;
}

.hero h1 {
    color: white;
    font-size: clamp(25px, 4vw, 38px);
    font-weight: 800;
    margin-bottom: 12px;
}

.hero p {
    color: #f7f1ff;
    font-size: 15px;
}

.section-title {
    color: #6846a7;
    font-size: 21px;
    font-weight: 800;
    margin: 25px 0 15px;
}

label {
    color: #594477 !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #fcfaff !important;
    color: #34264e !important;
    border: 1px solid #ded1f4 !important;
    border-radius: 12px !important;
    direction: rtl;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #9873d5 !important;
    box-shadow: 0 0 0 2px #e9ddff !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: #fcfaff;
    border-radius: 12px;
    border-color: #ded1f4;
}

.stButton button,
.stFormSubmitButton button,
.stDownloadButton button {
    background: linear-gradient(90deg, #8059ca, #a17bdc);
    color: white;
    border: none;
    border-radius: 13px;
    min-height: 44px;
    font-size: 14px;
    font-weight: 700;
    transition: .2s;
}

.stButton button:hover,
.stFormSubmitButton button:hover,
.stDownloadButton button:hover {
    background: #7047bb;
    color: white;
    border: none;
    transform: translateY(-2px);
}

.result {
    background: #f5f0ff;
    border: 1px solid #e3d4ff;
    border-radius: 16px;
    padding: 22px;
    margin-top: 20px;
    color: #49356b;
    line-height: 2;
}

.footer {
    text-align: center;
    color: #927eae;
    padding: 30px 0 10px;
    font-size: 12px;
}

div[data-testid="stExpander"] {
    border: 1px solid #ded1f4;
    border-radius: 14px;
    background: #fcfaff;
}

@media(max-width: 600px) {
    .block-container {
        padding: 1rem .7rem 2rem;
    }

    .hero {
        padding: 28px 15px;
        border-radius: 18px;
    }

    .section-title {
        font-size: 18px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# سربرگ
# ==========================================

st.markdown("""
<div class="hero">
    <h1>💜 دستیار هوشمند تولید محتوا</h1>
    <p>ایده‌های خلاقانه را به محتوای حرفه‌ای تبدیل کن.</p>
    <p>✨ قدرت فناوری در خدمت خلاقیت تو</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# موتور تولید محتوا
# ==========================================

def generate_content(topic, content_type, platform, tone, details):

    extra_info = (
        details.strip()
        if details.strip()
        else "توضیحات بیشتری ثبت نشده است."
    )

    if content_type == "سناریوی ریلز":

        output = f"""
🎬 عنوان سناریو:
{topic}

⏱ مدت پیشنهادی: ۳۰ ثانیه

🎯 قلاب شروع:
تا حالا به این فکر کردی که {topic} چقدر می‌تواند برای تو کاربردی باشد؟

🎙 بخش اول - شروع:
امروز می‌خواهیم درباره {topic} صحبت کنیم.

🎙 بخش دوم - آموزش:
اولین نکته مهم را بشناس.
سپس یک مثال کاربردی از آن را بررسی کن.
در نهایت یاد بگیر چطور از آن استفاده کنی.

🎙 بخش سوم - جمع‌بندی:
با چند قدم ساده می‌توانی اطلاعات بیشتری درباره این موضوع به دست بیاوری.

📢 دعوت به تعامل:
نظرت را در کامنت‌ها بنویس و این ویدئو را ذخیره کن.

📱 پلتفرم: {platform}
🎨 لحن: {tone}
📝 توضیحات: {extra_info}
"""

    elif content_type == "کپشن اینستاگرام":

        output = f"""
✨ {topic}

گاهی یادگیری یک موضوع جدید می‌تواند دیدگاه ما را تغییر دهد.

در این پست می‌خواهیم با {topic} بیشتر آشنا شویم و کاربردهای آن را بررسی کنیم.

💡 نکته مهم:
برای یادگیری بهتر، همیشه از مثال‌های واقعی استفاده کن.

💬 تو چه تجربه‌ای در این زمینه داری؟
نظرت را برای ما بنویس.

📌 این پست را ذخیره کن تا بعداً دوباره به آن مراجعه کنی.

#تولید_محتوا #آموزش #یادگیری #خلاقیت
"""

    elif content_type == "ایده تولید محتوا":

        output = f"""
💡 موضوع اصلی: {topic}

ایده اول:
معرفی {topic} برای افراد مبتدی

ایده دوم:
۵ نکته کاربردی درباره {topic}

ایده سوم:
اشتباهات رایج درباره {topic}

ایده چهارم:
آموزش مرحله‌به‌مرحله {topic}

ایده پنجم:
پاسخ به ۳ سؤال پرتکرار درباره {topic}

🎯 پیشنهاد:
برای شروع، ایده اول را به شکل یک ریلز آموزشی تولید کن.

📱 پلتفرم: {platform}
🎨 لحن: {tone}
"""

    elif content_type == "متن تبلیغاتی":

        output = f"""
✨ به دنبال راهی بهتر برای {topic} هستی؟

ما اینجاییم تا با ارائه راهکارهای مناسب، به تو کمک کنیم.

چرا این موضوع اهمیت دارد؟
• صرفه‌جویی در زمان
• دسترسی آسان‌تر
• تجربه بهتر

📩 برای دریافت اطلاعات بیشتر با ما در ارتباط باش.

📱 پلتفرم: {platform}
🎨 لحن: {tone}

توضیحات تکمیلی:
{extra_info}
"""

    elif content_type == "محتوای آموزشی":

        output = f"""
📚 عنوان آموزش:
آشنایی با {topic}

🔹 مقدمه:
در این آموزش می‌خواهیم با موضوع {topic} آشنا شویم.

🔹 بخش اول: معرفی موضوع
ابتدا مفهوم {topic} را بررسی می‌کنیم.

🔹 بخش دوم: کاربردها
کاربردهای مهم این موضوع را بشناسیم.

🔹 بخش سوم: تمرین عملی
یک نمونه ساده از {topic} را بررسی و اجرا کنیم.

🔹 جمع‌بندی:
با یادگیری اصول و تمرین مستمر می‌توانیم در این زمینه پیشرفت کنیم.

📱 پلتفرم: {platform}
🎨 لحن: {tone}

توضیحات تکمیلی:
{extra_info}
"""

    return output


# ==========================================
# ساخت محتوای جدید
# ==========================================

st.markdown(
    '<div class="section-title">✦ ساخت محتوای جدید</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    with st.form("content_form"):

        topic = st.text_input(
            "موضوع محتوای خود را وارد کنید",
            placeholder="مثلاً: کاربرد هوش مصنوعی در زندگی روزمره"
        )

        col1, col2 = st.columns(2)

        with col1:
            content_type = st.selectbox(
                "نوع محتوا",
                CONTENT_TYPES
            )

        with col2:
            platform = st.selectbox(
                "پلتفرم انتشار",
                PLATFORMS
            )

        tone = st.selectbox(
            "لحن محتوا",
            TONES
        )

        details = st.text_area(
            "توضیحات بیشتر (اختیاری)",
            placeholder="مخاطب هدف و جزئیات موردنظر خود را بنویسید..."
        )

        submitted = st.form_submit_button(
            "✨ تولید محتوا",
            use_container_width=True
        )


if submitted:

    if topic.strip():

        with st.spinner("در حال آماده‌سازی محتوا..."):

            output = generate_content(
                topic,
                content_type,
                platform,
                tone,
                details
            )

        history = load_history()

        new_item = {
            "id": str(uuid4()),
            "date": datetime.now().strftime("%Y/%m/%d - %H:%M"),
            "topic": topic.strip(),
            "content_type": content_type,
            "platform": platform,
            "tone": tone,
            "details": details.strip(),
            "output": output
        }

        history.insert(0, new_item)

        if save_history(history):
            st.session_state["latest_output"] = output
            st.success("محتوا با موفقیت تولید و در تاریخچه ذخیره شد.")

    else:
        st.warning("لطفاً ابتدا موضوع محتوا را وارد کن.")


# ==========================================
# نمایش آخرین محتوای تولیدشده
# ==========================================

if st.session_state.get("latest_output"):

    st.markdown(
        '<div class="section-title">✦ آخرین محتوای تولیدشده</div>',
        unsafe_allow_html=True
    )

    latest_output = st.session_state["latest_output"]

    st.code(latest_output, language=None)

    st.download_button(
        "⬇️ دانلود محتوای تولیدشده",
        data=latest_output,
        file_name="content_output.txt",
        mime="text/plain",
        key="download_latest",
        use_container_width=True
    )


# ==========================================
# تاریخچه محتواها
# ==========================================

st.markdown(
    '<div class="section-title">✦ مدیریت تاریخچه محتواها</div>',
    unsafe_allow_html=True
)

history = load_history()

if history:

    st.caption(
        f"تعداد کل محتواهای ذخیره‌شده: {len(history)}"
    )

    # --------------------------------------
    # جست‌وجو و فیلتر
    # --------------------------------------

    st.markdown("### 🔎 جست‌وجو و دسته‌بندی")

    search_text = st.text_input(
        "جست‌وجو در عنوان یا متن محتوا",
        placeholder="موضوع یا بخشی از متن را وارد کن..."
    )

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        type_filter = st.selectbox(
            "فیلتر بر اساس نوع محتوا",
            ["همه"] + CONTENT_TYPES,
            key="type_filter"
        )

    with filter_col2:
        platform_filter = st.selectbox(
            "فیلتر بر اساس پلتفرم",
            ["همه"] + PLATFORMS,
            key="platform_filter"
        )

    filtered_history = []

    for item in history:

        if type_filter != "همه":
            if item.get("content_type") != type_filter:
                continue

        if platform_filter != "همه":
            if item.get("platform") != platform_filter:
                continue

        if search_text.strip():
            searchable_text = (
                str(item.get("topic", "")) + " " +
                str(item.get("output", ""))
            ).casefold()

            if search_text.strip().casefold() not in searchable_text:
                continue

        filtered_history.append(item)

    st.caption(
        f"تعداد نتایج پیدا شده: {len(filtered_history)}"
    )

    # --------------------------------------
    # نمایش، ویرایش و حذف تکی
    # --------------------------------------

    for index, item in enumerate(filtered_history):

        item_id = str(item.get("id", index))

        title = (
            f"📝 {item.get('topic', 'بدون عنوان')} | "
            f"{item.get('date', '')}"
        )

        with st.expander(title):

            st.write(
                f"**نوع محتوا:** {item.get('content_type', '')}"
            )

            st.write(
                f"**پلتفرم:** {item.get('platform', '')}"
            )

            st.write(
                f"**لحن:** {item.get('tone', '')}"
            )

            st.write(
                f"**توضیحات:** {item.get('details', 'ندارد') or 'ندارد'}"
            )

            st.divider()

            # متن قابل ویرایش
            edited_output = st.text_area(
                "متن محتوا (برای ویرایش، متن را تغییر بده)",
                value=item.get("output", ""),
                height=260,
                key=f"edit_text_{item_id}"
            )

            col_save, col_download = st.columns(2)

            with col_save:

                if st.button(
                    "💾 ذخیره ویرایش",
                    key=f"save_{item_id}",
                    use_container_width=True
                ):

                    current_history = load_history()
                    target = find_item(current_history, item_id)

                    if target is not None:
                        target["output"] = edited_output

                        if save_history(current_history):
                            st.success("ویرایش با موفقیت ذخیره شد.")
                            st.rerun()
                    else:
                        st.error("این محتوا در تاریخچه پیدا نشد.")

            with col_download:

                st.download_button(
                    "⬇️ دانلود محتوا",
                    data=edited_output,
                    file_name=f"content_{item_id[:8]}.txt",
                    mime="text/plain",
                    key=f"download_{item_id}",
                    use_container_width=True
                )

            st.divider()

            # حذف تکی با تأیید
            delete_confirm = st.checkbox(
                "از حذف این محتوا مطمئن هستم",
                key=f"confirm_delete_{item_id}"
            )

            if st.button(
                "🗑️ حذف این محتوا",
                key=f"delete_{item_id}",
                disabled=not delete_confirm,
                use_container_width=True
            ):

                current_history = load_history()

                updated_history = [
                    x for x in current_history
                    if str(x.get("id")) != item_id
                ]

                if len(updated_history) < len(current_history):

                    if save_history(updated_history):
                        st.success("محتوا حذف شد.")
                        st.rerun()

                else:
                    st.error("محتوای موردنظر پیدا نشد.")

    # --------------------------------------
    # حذف کل تاریخچه
    # --------------------------------------

    st.divider()

    st.markdown("### ⚠️ پاک‌سازی تاریخچه")

    clear_confirm = st.checkbox(
        "تمام محتواهای ذخیره‌شده حذف شوند",
        key="confirm_clear_all"
    )

    if st.button(
        "🗑️ پاک کردن تمام تاریخچه",
        disabled=not clear_confirm,
        use_container_width=True
    ):

        if save_history([]):
            st.session_state.pop("latest_output", None)
            st.success("تمام تاریخچه پاک شد.")
            st.rerun()

else:

    st.info(
        "هنوز محتوایی در تاریخچه ذخیره نشده است. "
        "پس از تولید محتوا، نتیجه در این بخش نمایش داده می‌شود."
    )


# ==========================================
# توضیح نسخه فعلی
# ==========================================

st.divider()

st.info(
    "این نسخه آزمایشی از قالب‌های برنامه‌نویسی Python "
    "برای تولید متن استفاده می‌کند. هنوز به مدل هوش مصنوعی "
    "واقعی متصل نشده است."
)


# ==========================================
# پابرگ
# ==========================================

st.markdown("""
<div class="footer">
    طراحی و توسعه با خلاقیت 💜<br>
    AI Content Assistant | Powered by Python
</div>
""", unsafe_allow_html=True)
