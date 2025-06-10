import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
from backend.services.transcript_logger import clean_transcript

def render():
    # st.title("Your Dashboard Title")
    # rest of your Streamlit UI

    st.title("🕷️ Developer Log Explorer")

    # Choose which log file
    log_choice = st.selectbox(
        "Select Log Type:",
        ("Transcripts", "Venue Mentions", "Parsed Events")
    )

    # Load the selected log
    if log_choice == "Transcripts":
        df = pd.read_csv("data/logs/all_transcripts.csv")
        filtered_df, selected_date = filter_df(df)
        filtered_df.drop_duplicates(inplace=True)
        filtered_df = filtered_df.sort_values("timestamp", ascending=True)
        # if log_choice == "Transcripts":
        #     df["transcript_clean"] = df["transcript"].apply(clean_transcript)
            
        # columns_to_display = ["timestamp_parsed", "cleaned"]

        # display_columns = ["timestamp_parsed", ]

        # # Display full-width
        # st.dataframe(
        #     filtered_df[columns_to_display],
        #     use_container_width=True,
        #     hide_index=True
        # )

        # # (Optional) Expand individual entries for cleaner reading
        # for i, row in filtered_df.iterrows():
        #     with st.expander(f"{row['timestamp']} — {row.get('station', 'Unknown')}"):
        #         st.write(row.to_dict())
        st.subheader(f"🕑 Logs for {selected_date}")

        log_lines = []

        last_hour = None

        for _, row in filtered_df.iterrows():
            timestamp = row.get("timestamp_parsed", "Unknown Time")
            transcript = row.get("cleaned", "(No transcript available)")
            venue_flag = row.get("contains_venue", False)

            if not pd.isna(transcript):
                # Parse hour from timestamp
                if timestamp != "Unknown Time":
                    hour = pd.to_datetime(timestamp).hour
                    time_str = pd.to_datetime(timestamp).strftime("%H:%M:%S")
                else:
                    hour = None

                # 🕛 If new hour, insert a big heading
                if hour != last_hour and hour is not None:
                    log_lines.append(
                        f"<h2 style='color:#ffaa00;'>🕛 {hour:02d}:00</h2>\n"
                    )
                    last_hour = hour

                # Color timestamp based on venue flag
                if venue_flag:
                    time_display = f"<div style='color:orange; font-weight:bold;'>🏟️ {time_str} — Venue mentioned</div>"
                else:
                    time_display = f"<div style='color:lightgreen; font-weight:bold;'>🕑 {time_str}</div>"

                # 🛠️ Use the correctly styled time_display here
                log_lines.append(
                    f"{time_display}\n{transcript}\n<hr style='border:1px dashed #444;'>\n"
                )


        # Combine all
        full_log = "\n".join(log_lines)

        # Display it
        st.markdown(
            full_log,
            unsafe_allow_html=True
        )
        components.html(
            """
            <style>
            ::-webkit-scrollbar {
                width: 12px;
            }
            ::-webkit-scrollbar-thumb {
                background-color: rgba(100, 100, 100, 0.6);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.1);
            }
            </style>
            """,
            height=0,
        )

    elif log_choice == "Venue Mentions":
        df = pd.read_csv("data/logs/venue_mentions.csv")
    else:
        df = pd.read_csv("data/logs/parsed_events.csv")







def filter_df(df):
    # Parse timestamps, forcing bad ones to NaT
    df["timestamp_parsed"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Count how many were invalid
    num_invalid_timestamps = df["timestamp_parsed"].isna().sum()
    st.info(f"📄 Invalid timestamps detected and dropped: {num_invalid_timestamps}")

    # Continue clean flow
    df["date"] = df["timestamp_parsed"].dt.date

    # unique_dates = df["date"].dropna().unique()
    unique_dates = sorted(df["date"].dropna().unique(), reverse=False)


    # Date filter
    selected_date = st.selectbox("Select Date:", sorted(unique_dates),index=len(unique_dates) - 1)


    # Filter dataframe on selected date
    filtered_df = df[df["date"] == selected_date]


    return filtered_df, selected_date
