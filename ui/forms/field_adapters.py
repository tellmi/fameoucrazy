# ui/forms/field_adapters.py
# -*- coding: utf-8 -*-


from PySide6.QtCore import QDate, Qt

def text_field():
    return {
        "getter": lambda w: str(w.text().strip()),
        "setter": lambda w, v: w.setText("" if v is None else str(v))
    }

def combo_field():
    return {
        "getter": lambda w: str(w.currentText()),
        "setter": lambda w, v: w.setCurrentText("" if v is None else str(v))
    }

def radio_field(radio_dict):
    """radio_dict: {value: QRadioButton}"""
    return {
        "getter": lambda _: next((k for k, rb in radio_dict.items() if rb.isChecked()), ""),
        "setter": lambda _, v: [rb.setChecked(k==v) for k, rb in radio_dict.items()]
    }

def toggle_field():
    return {
        "getter": lambda w: str(w.isChecked()),
        "setter": lambda w, v: w.setChecked(v.lower() == "true" if isinstance(v, str) else bool(v))
    }

def date_field():
    # same as text_field, but kept for semantic distinction
    return {
        "getter": lambda w: w.date().toString("dd.MM.yyyy") if w else "",
        "setter": lambda w, v: w.setDate(QDate.fromString(v, "dd.MM.yyyy")) if w and v else None
    }

def password_field():
    return {
        "getter": lambda w: w.text().strip() if w else "",
        "setter": lambda w, v: w.setText(str(v) if v is not None else ""),
        "init": lambda w: w.setEchoMode(QLineEdit.Password) if w else None
    }
