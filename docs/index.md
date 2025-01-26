---
layout: home
---

<h1>Transform Your Codebase with AI</h1>
<p class="lead">Semantic code modifications through natural language</p>

<div class="example">
<pre><code class="console">gptdiff "Add type hints to functions" --apply
</code></pre>
<div class="success">✅ Successfully applied patch</div>
</div>

<div class="example">
<pre><code class="console">gptdiff "Add API documentation" --call
</code></pre>
<div class="info">🔧 Patch written to diff.patch</div>
</div>

<div class="example">
<pre><code class="console">gptdiff "Improve error messages"
</code></pre>
<div class="info">📄 LLM not called, written to prompt.txt</div>
</div>

<div class="toolbox-note">🔧 Part of the <a href="https://github.com/255BITS/ai-agent-toolbox">AI Agent Toolbox</a> ecosystem - simplifying AI tool usage across models and frameworks</div>
---

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
      <li>Test changes first</li>
    </ul>
  </li>
</ul>

## Getting Started
<pre><code class="console">
$ pip install gptdiff
</code></pre>