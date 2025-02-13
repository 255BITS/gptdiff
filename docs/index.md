

<h1>Create and apply diffs with AI</h1>
<p class="lead">Modify projects with natural language</p>

<div class="example">
<pre><code class="console">gptdiff "Add button animations on press" --apply
<div class="success">✅ Successfully applied patch</div></code></pre>
</div>

<div class="example">
<pre><code class="console">gptdiff "Add API documentation" --call
<div class="info">🔧 Patch written to diff.patch</div></code></pre>
</div>

<div class="example">
<pre><code class="console">gptdiff "Improve error messages"
<div class="info">📄 LLM not called, written to prompt.txt</div></code></pre>
</div>

<div class="example">
<pre><code class="console">gptdiff "Improve login error messages" auth.py --apply
<div class="success">✅ Patch applied: auth.py updated successfully</div></code></pre>
</div>

<p class="lead">Set up agents loops with simple bash commands</p>

```bash
while
do
  gptdiff "Add missing test cases" --apply
done
```

[open source and MIT licensed at github.com/255BITS/gptdiff](https://github.com/255BITS/gptdiff)

<iframe width="560" height="315" src="https://www.youtube.com/embed/cmEMSCQRWto" frameborder="0" allowfullscreen></iframe>

<div class="feature command-feature">
  <h3>🚀 Make impactful changes with one command</h3>
  <ul class="feature-list">
    <li><code>--apply</code> AI-powered patch recovery</li>
    <li><code>--nobeep</code> Disable completion notifications</li>
    <li><code>--temperature</code> Control creativity (0-2)</li>
    <li><code>--model</code> Switch between LLM providers</li>
  </ul>
</div>

## Features

<ul class="features">
  <li class="feature">
    <strong>🔥 Multi-File Changes</strong> - Update related files together in one step
  </li>
  
  <li class="feature">
    <strong>🛠 Auto-Fix Conflicts</strong><br>
    Fixes conflicting changes using AI understanding of your code's purpose
  </li>
  
  <li class="feature">
    <strong>⚡ Simple Commands</strong>
    <ul>
      <li>Change specific files</li>
      <li>See progress updates</li>
      <li>Clear cost tracking</li>
    </ul>
  </li>

  <li class="feature">
    <strong>🎯 Uses .gitignore and .gptignore</strong><br>
    Exclude files by efficient pattern matching
  </li>
  
</ul>

## How to develop with gptdiff

<div class="git-workflow">
  <h3 class="workflow-title">🚀 The new dev cycle</h3>
  
  <ol class="workflow-steps">
    <li class="workflow-step">
      <h4 class="step-heading">Generate Changes</h4>
      <div class="code-block">
        <pre><code class="console">gptdiff "Add type safety" --apply</code></pre>
      </div>
    </li>

    <li class="workflow-step">
      <h4 class="step-heading">Review Modifications</h4>
      <div class="code-block">
        <pre><code class="console">git add -p</code></pre>
      </div>
    </li>

    <li class="workflow-step">
      <h4 class="step-heading">Finalize Changes</h4>
      <div class="code-block">
        <pre><code class="console">git commit -m 'AI improvements'</code></pre>
      </div>
    </li>

    <li class="workflow-step">
      <h4 class="step-heading">Stash Uncommitted Changes</h4>
      <div class="code-block">
        <pre><code class="console">git stash</code></pre>
      </div>
    </li>
  </ol>
</div>

## Getting Started
For a step-by-step guide on how to install and configure `gptdiff`, check out the [Installation Guide](installation.md).

```bash
$ pip install gptdiff
```

<div class="toolbox-note">🔧 Built with <a href="https://toolbox.255labs.xyz">AI Agent Toolbox</a></div>

## Using gptpatch

You can further refine your diff application using gptpatch. For example, to enhance clarity:

    gptdiff "make the value prop clearer" splash.html

Then, copy the generated prompt from prompt.txt to your clipboard and send it to OpenAI. Once you receive the outputs, open patch.diff, paste the outputs, and finally run:

    gptpatch patch.diff

Note: You can configure GPTDIFF_SMARTAPPLY_* variables independently from the base GPTDIFF_* variables.