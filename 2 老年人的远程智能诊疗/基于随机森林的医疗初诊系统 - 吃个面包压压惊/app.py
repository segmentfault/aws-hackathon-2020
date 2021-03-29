from flask import Flask, render_template, redirect, session
from form import Form
from diagnosis import get_disease

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = Form()
    if form.validate_on_submit():
        session['result'] = get_disease(form.symptom.data)
        return redirect('/')

    return render_template('base.html',
                           title='基于随机森林的医疗初诊系统',
                           form=form,
                           result=session.get('result'))


if __name__ == '__main__':
    app.run()
