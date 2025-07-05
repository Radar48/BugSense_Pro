from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from .scanners import run_nmap_scan
from .fuzzer import dir_fuzz


main = Blueprint("main", __name__)


@main.route("/")
def home():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template("home.html")

@main.route('/scan', methods=['POST'])
def scan():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    target = request.form.get('target')
    result = run_nmap_scan(target)
    return render_template('home.html', result=result, target=target, user=session['user'])

@main.route('/fuzz', methods=['POST'])
def fuzz():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    target = request.form.get('target')
    wordlist = list(set(['admin', 'login', 'backup', 'config', 'test', 'dashboard', '.git', 'test', 'api', 'uploads']))
    results = dir_fuzz(target, wordlist)
    return render_template('home.html', fuzz_results=results, target=target, user=session['user'])

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'bugsense2025':
            session['user'] = username
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))

@main.route('/clear', methods=['POST'])
def clear():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template("home.html", result=None, fuzz_results=[], target=None, user=session['user'])

@main.route('/download', methods=['POST'])
def download():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    result = request.form.get('result')
    fuzz_results = request.form.get('fuzz_results')
    content = ""
    if result:
        content += "=== Nmap Scan Results ===\n"
        content += result +"\n\n"
    if fuzz_results:
        content += "=== Directory Scan Results ===\n"
        content += fuzz_results +"\n"
    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=bugsense_results.txt"
    response.headers["Content-Type"] = "text/plain"

    return response