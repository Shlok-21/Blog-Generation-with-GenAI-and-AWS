from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/blog', methods = ['POST'])
def generate_blog():
    blog_topic = request.form['blogTitle']
    blog_content = f'Generated content for blog title {blog_topic}'
    return render_template('result.html', blog_title=blog_topic, blog_content=blog_content)


if __name__ == '__main__':
    app.run(debug=True)