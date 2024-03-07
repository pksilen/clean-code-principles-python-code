import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
  <div>
    <todos-table-view></todos-table-view>
  </div>`,
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular-test';
}
