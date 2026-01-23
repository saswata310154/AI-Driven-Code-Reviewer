# 🤖 AI-Powered Code Reviewer

![Project Logo](logo.png)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-driven-code-reviewer.streamlit.app/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org)

> **An intelligent web application that reviews Python code, detects issues, and suggests improvements using AI.**  
> Developed as part of the *Infosys Springboard Virtual Internship Program*.

---

## 📌 Overview

**AI-Powered Code Reviewer** is a web-based tool designed to help developers write cleaner, more efficient Python code.  
The application performs static analysis, detects errors, checks coding standards, and provides AI-generated recommendations using a large language model.

The goal of this project is to **automate the code review process** and deliver quick, meaningful feedback to developers and students.

---

## 🌍 Live Application

Try the deployed version here:  
👉 **https://ai-driven-code-reviewer-saswata-sarkar.streamlit.app/**

---

## ✨ Features

- 🔎 **Code Structure Analysis** using Abstract Syntax Trees (AST)
- 🐞 **Error Detection** for syntax and common logical issues
- 🎯 **PEP-8 Style Validation** for clean and readable code
- 🧠 **AI-Based Suggestions** powered by Qwen 2.5 LLM
- 💬 **Interactive Chat Interface** to ask questions about your code
- 📊 **AST Visualization** for better understanding of code flow

---

## 🧰 Technology Stack

- **Language**: Python 3.11  
- **Frontend**: Streamlit  
- **AI Model**: Qwen/Qwen2.5-7B-Instruct (Hugging Face API)  
- **Code Analysis**: Python AST, Pylint  
- **Version Control**: Git & GitHub  

---

## 📁 Repository Layout

```text
AI-Driven-Code-Reviewer/
├── app.py                  # Streamlit application entry point
├── chatbot.py              # AI chatbot logic
├── ai_suggester.py         # LLM integration module
├── code_parser.py          # AST parsing utilities
├── error_detector.py       # Static error detection
├── style_checker.py        # PEP-8 style checks
├── requirements.txt        # Project dependencies
└── logo.png                # Application logo
