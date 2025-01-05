# Random Chess Bot Version 2
This is version 2 of random chess bot.

Version 2 is more efficient than version 1 by implementing the following:
- Implemented class inheritance.
- Added validation to eliminate moves that would put the player in check.
- Ditched `pyautogui` in favor of `selenium` web browser.
- Web scraping help accomplished with `beautifulsoup`.
- Added login validation and cookie saving & loading.
- By implementing `rich`, the whole thing can be viewed and played in a terminal.

# Running with docker
```
docker build -t chess-bot .
docker run -it -v C:/Users/User/.chess_login:/app/src/logins --name chess-bot chess-bot
docker start -ai chess-bot
```

## Random Chess Bot Version 1
[Link to version 1 of random chess bot](https://github.com/Jampamane/Random_Chess_1.0)


<div>
  <input type="radio" id="tab1" name="tab" checked>
  <label for="tab1">Windows</label>
  <input type="radio" id="tab2" name="tab">
  <label for="tab2">Linux</label>

  <div class="tab-content" id="content1">
    <pre><code class="language-python">
print("poop")
    </code></pre>
  </div>

  <div class="tab-content" id="content2">
    <pre><code class="language-python">
print("wow")
    </code></pre>
  </div>
</div>

<style>
  input[name="tab"] {
    display: none;
  }

  label {
    display: inline-block;
    padding: 10px;
    background: #ddd;
    cursor: pointer;
  }

  label:hover {
    background: #bbb;
  }

  input:checked + label {
    background: #bbb;
  }

  .tab-content {
    display: none;
    padding: 10px;
    border: 1px solid #ddd;
  }

  #tab1:checked ~ #content1,
  #tab2:checked ~ #content2 {
    display: block;
  }
</style>
