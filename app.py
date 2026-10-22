"""Suno A/B Lab: privacy-first, local blind audio comparison MVP."""
import csv
import hashlib
import io
import itertools
import random
import streamlit as st
from audio import decode_audio, measure_audio, preview_wav
from ranking import elo_update

st.set_page_config(page_title='Suno A/B Lab', page_icon='🎧', layout='wide')
st.title('Suno A/B Lab')
st.caption('Blind listening comparisons and technical audio measurements. No automatic artistic-quality claims.')
st.info('Files are processed in the Streamlit server process. For privacy, run locally: streamlit run app.py. Avoid deploying with sensitive audio to a third-party server.')
files = st.file_uploader('Upload 2–10 WAV/FLAC/OGG files', type=['wav','flac','ogg'], accept_multiple_files=True)
if not files or len(files) < 2:
    st.stop()
if len(files) > 10:
    st.error('Maximum 10 files.')
    st.stop()

tracks = {}
for f in files:
    try:
        raw = f.getvalue()
        if len(raw) > 60 * 1024 * 1024:
            st.warning(f'{f.name}: exceeds 60 MB; skipped')
            continue
        key = hashlib.sha256(raw).hexdigest()
        if key in tracks:
            st.warning(f'{f.name}: duplicate audio skipped')
            continue
        samples, rate = decode_audio(raw)
        tracks[key] = {'name':f.name, 'raw':raw, 'metrics':measure_audio(samples,rate), 'preview':preview_wav(samples,rate)}
    except Exception as exc:
        st.warning(f'{f.name}: unsupported or corrupt audio ({type(exc).__name__})')
if len(tracks) < 2:
    st.error('At least two distinct valid files are required.')
    st.stop()

ids = sorted(tracks)
session_id = hashlib.sha256('|'.join(ids).encode()).hexdigest()
if st.session_state.get('session_id') != session_id:
    st.session_state.session_id = session_id
    st.session_state.ratings = {key: 1000.0 for key in ids}
    st.session_state.votes = []
    st.session_state.pairs = list(itertools.combinations(ids, 2))
    random.shuffle(st.session_state.pairs)
    st.session_state.index = 0

st.subheader('Blind A/B listening')
if st.session_state.index < len(st.session_state.pairs):
    a, b = st.session_state.pairs[st.session_state.index]
    st.write(f'Comparison {st.session_state.index + 1} of {len(st.session_state.pairs)}')
    left, right = st.columns(2)
    with left:
        st.markdown('**Version A**')
        st.audio(tracks[a]['preview'], format='audio/wav')
    with right:
        st.markdown('**Version B**')
        st.audio(tracks[b]['preview'], format='audio/wav')
    selection = st.radio('Which is better?', ['A', 'B', 'Tie'], horizontal=True, key=f'vote_{st.session_state.index}')
    if st.button('Record vote', type='primary'):
        choice = {'A':'a','B':'b','Tie':'tie'}[selection]
        st.session_state.ratings[a], st.session_state.ratings[b] = elo_update(st.session_state.ratings[a],st.session_state.ratings[b],choice)
        st.session_state.votes.append({'a':a,'b':b,'choice':choice})
        st.session_state.index += 1
        st.rerun()
else:
    st.success('All comparisons completed.')

st.subheader('Results')
rows = []
for key in ids:
    rows.append({'File':tracks[key]['name'], 'Elo':round(st.session_state.ratings[key],1), **tracks[key]['metrics']})
rows.sort(key=lambda r:r['Elo'], reverse=True)
st.dataframe(rows, use_container_width=True, hide_index=True)
st.caption('Elo is a preference ranking from your votes, not a scientifically validated measure of musical quality. Metrics such as RMS and crest factor are descriptive only.')
if st.session_state.votes:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    st.download_button('Export CSV', output.getvalue(), file_name='suno_ab_results.csv', mime='text/csv')
if st.button('Restart comparisons'):
    del st.session_state.session_id
    st.rerun()
