import * as React from 'react';

import {
  Dialog
} from '@jupyterlab/apputils';


export class FunctionTable extends React.Component<any> {
  data: any
  delegate: any
  constructor(data: any, delegate: any){
    super(data, delegate)
    this.data = data
    this.delegate = delegate
  }
  delete(name: string){
    this.delegate.delete(name)
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
                <td><button className={'fa fa-trash'} onClick={() => this.delete(item.name)}></button></td>
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
            <th>Delete</th>
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

  constructor(data: any, delegate: any) {
    this.title = 'Function List'
    this.body = new FunctionTable(data, delegate).render()
  }
}

