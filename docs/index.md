---
layout: home
---

<div class="toolbox-note">🔧 Part of the <a href="https://github.com/255BITS/ai-agent-toolbox">AI Agent Toolbox</a> ecosystem - simplifying AI tool usage across models and frameworks</div>

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

---

<div class="feature command-feature">
  <h3>🚀 Make impactful changes with one command</h3>
  <ul class="feature-list" style="width: 100%">
    <li><code>--apply</code> AI-powered patch recovery</li>
    <li><code>--nobeep</code> Disable completion notifications</li>
    <li><code>--temperature</code> Control creativity (0-2)</li>
    <li><code>--model</code> Switch between LLM providers</li>
  </ul>
</div>

## Features

<ul class="features">
  <li class="feature">
    <strong>🔥 Cross-File Refactoring</strong> - Make coordinated changes across multiple files in a single operation
  </li>
  
  <li class="feature">
    <strong>🛠 Smart Conflict Resolution</strong><br>
    Automatically resolves patch conflicts using AI context understanding while maintaining code integrity
  </li>
  
  <li class="feature">
    <strong>⚡ CLI Excellence</strong>
    <ul>
      <li>Surgical file targeting</li>
      <li>Real-time progress tracking</li>
      <li>Token usage & cost transparency</li>
      <li>Dry-run validation mode</li>
    </ul>
  </li>
</ul>

## Getting Started
<pre><code class="console">
$ pip install gptdiff
</code></pre>