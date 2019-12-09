import * as React from 'react';

import {
  Dialog
} from '@jupyterlab/apputils';


export class FunctionTable extends React.Component<any> {
  data: any
  constructor(data: any){
    super(data)
    this.data = data
  }
  getTableBodyAsReactElement(data: any) {
    return (!data) ? null : (
        <tbody>
        {data.map((item: any) => {
          console.log('item: ', item);
          return (
              <tr>
              <td>{item.name}</td>
              <td>{item.trigger}</td>
              <td>{item.success}</td>
              <td>{item.fail}</td>
              </tr>
              )
        })}
        </tbody>
    );
  }
  render() {
    return (
        <table >
          <thead>
          <tr>
            <th>Name</th>
            <th>Triggered</th>
            <th>Success</th>
            <th>Fail</th>
          </tr>
          </thead>
          {this.getTableBodyAsReactElement(this.data)}
        </table>
    );
  }
}

export class FunctionDialog implements Dialog.IOptions<React.ReactElement<any>> {
  title: Dialog.Header;
  body: Dialog.Body<React.ReactElement<any>>;
  host: HTMLElement;
  buttons: ReadonlyArray<Dialog.IButton>;
  defaultButton: number;
  focusNodeSelector: string;
  renderer: Dialog.IRenderer;

  constructor(data: any) {
    this.title = 'Function List'
    this.body = new FunctionTable(data).render()
  }
}

