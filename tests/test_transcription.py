from tor_log_analyzer.transcription import extract_components, extract_format_and_type


def test_extract_components_from_simple_comment():
    header, content, footer = extract_components("""*Image Transcription: Tumblr*

---

[*Description.*]

---

^^I'm&#32;a&#32;human&#32;volunteer&#32;content&#32;transcriber&#32;for&#32;Reddit&#32;and&#32;you&#32;could&#32;be&#32;too!&#32;[If&#32;you'd&#32;like&#32;more&#32;information&#32;on&#32;what&#32;we&#32;do&#32;and&#32;why&#32;we&#32;do&#32;it,&#32;click&#32;here!](https://www.reddit.com/r/TranscribersOfReddit/wiki/index)""")

    assert header == "*Image Transcription: Tumblr*"
    assert content == "[*Description.*]"
    assert footer == """^^I'm&#32;a&#32;human&#32;volunteer&#32;content&#32;transcriber&#32;for&#32;Reddit&#32;and&#32;you&#32;could&#32;be&#32;too!&#32;[If&#32;you'd&#32;like&#32;more&#32;information&#32;on&#32;what&#32;we&#32;do&#32;and&#32;why&#32;we&#32;do&#32;it,&#32;click&#32;here!](https://www.reddit.com/r/TranscribersOfReddit/wiki/index)"""


def test_extract_components_from_comment_with_separators():
    header, content, footer = extract_components("""*Image Transcription: Tumblr*

---

[*Description 1.*]

---

[*Description 2.*]

---

^^I'm&#32;a&#32;human&#32;volunteer&#32;content&#32;transcriber&#32;for&#32;Reddit&#32;and&#32;you&#32;could&#32;be&#32;too!&#32;[If&#32;you'd&#32;like&#32;more&#32;information&#32;on&#32;what&#32;we&#32;do&#32;and&#32;why&#32;we&#32;do&#32;it,&#32;click&#32;here!](https://www.reddit.com/r/TranscribersOfReddit/wiki/index)""")

    assert header == "*Image Transcription: Tumblr*"
    assert content == """[*Description 1.*]

---

[*Description 2.*]"""
    assert footer == """^^I'm&#32;a&#32;human&#32;volunteer&#32;content&#32;transcriber&#32;for&#32;Reddit&#32;and&#32;you&#32;could&#32;be&#32;too!&#32;[If&#32;you'd&#32;like&#32;more&#32;information&#32;on&#32;what&#32;we&#32;do&#32;and&#32;why&#32;we&#32;do&#32;it,&#32;click&#32;here!](https://www.reddit.com/r/TranscribersOfReddit/wiki/index)"""


def test_extract_format_and_type_for_twitter():
    header = "*Image Transcription: Twitter*"
    t_format, t_type = extract_format_and_type(header)

    assert t_format == "Image"
    assert t_type == "Twitter"


def test_extract_format_and_type_for_video():
    header = "*Video Transcription:*"
    t_format, t_type = extract_format_and_type(header)

    assert t_format == "Video"
    assert t_type == "Video"


def test_extract_format_and_type_for_gif():
    header = "*Image Transcription: GIF*"
    t_format, t_type = extract_format_and_type(header)

    assert t_format == "GIF"
    assert t_type == "GIF"
