import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-visualizer',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './visualizer.component.html',
  styleUrls: ['./visualizer.component.css']
})
export class VisualizerComponent {
  code: string = '';
  selectedLanguage: string = 'python';
  resultType: string = '';
  resultContent: string = '';
  sanitizedHtml: SafeHtml | null = null;
  errorMessage: string = '';

  constructor(private sanitizer: DomSanitizer) {}

  runCode() {
    this.errorMessage = '';
    const payload = {
      language: this.selectedLanguage,
      code: this.code
    };
  
    fetch('http://localhost:5050/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        if (data.type === 'error') {
          this.resultType = 'error';
          this.resultContent = '';
          this.errorMessage = data.content || 'Unknown error occurred.';
        } else {
          this.resultType = data.type;
          this.resultContent = data.content;
      
          if (data.type === 'html') {
            this.sanitizedHtml = this.sanitizer.bypassSecurityTrustHtml(data.content);
          }
        }
      })
      
      .catch(err => {
        this.resultType = 'error';
        this.errorMessage = err.message || 'Request failed.';
      });
  }
}  
