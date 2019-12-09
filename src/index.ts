import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';

// import {
//   ICommandPalette
// } from '@jupyterlab/apputils';

import {
  IStateDB, URLExt
} from '@jupyterlab/coreutils'

import {
  ServerConnection,
} from '@jupyterlab/services';

import {
  IDisposable, DisposableDelegate
} from '@phosphor/disposable';

import {
  ToolbarButton, showErrorMessage, showDialog
} from '@jupyterlab/apputils';

import {
  DocumentRegistry
} from '@jupyterlab/docregistry';

import {
  NotebookPanel, INotebookModel
} from '@jupyterlab/notebook';
import {JSONObject} from "@phosphor/coreutils";
import {FunctionDialog} from "./dialog";

/**
 * Initialization data for the jupyter-lab-serverless extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-lab-serverless',
  requires: [IStateDB],
  autoStart: true,
  activate: activate
};

interface Response extends JSONObject{
  code: string
  msg: string
  data: any
}

// interface Function extends JSONObject {
//   name: string;
//   script: string;
//   raw: string;
//   trigger: number;
//   cost: number;
//   success: number;
//   fail: number;
//   created: string;
//   updated: string;
// }

/**
 * Make a request to the notebook server FunctionHandler endpoint.
 *
 * @param name function name.
 *
 * @param settings - the settings for the current notebook server.
 *
 * @returns a Promise resolved with the JSON response.
 */
function FunctionRequest(
    path: string,
    settings: ServerConnection.ISettings
): Promise<Response> {
  let url = URLExt.join(settings.baseUrl, 'function');
  let requestInit: RequestInit = {method: 'GET', body: null}
  if (path != null){
    requestInit.method = 'PUT'
    url = URLExt.join(url, path)
  }

  return ServerConnection.makeRequest(url, requestInit, settings).then(response => {
    if (response.status !== 200) {
      return response.text().then(data => {
        showErrorMessage("Save Function Error", data)
        // throw new ServerConnection.ResponseError(response, data);
      });
    }
    return response.json().then(json => {
      return json
    });
  });
}

/**
 * Save Current Script as A Serverless Function
 */
export
class ButtonExtensionAdd implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {

  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    let callback = () => {
      const serverSettings = ServerConnection.makeSettings();
      FunctionRequest(encodeURIComponent(context.path), serverSettings).then((data: any)=>{
            showErrorMessage("Save Function Success", '')
            console.log(data)
          }
      )
    };
    let button = new ToolbarButton({
      className: 'serverless-add',
      iconClassName: 'fa fa-desktop',
      onClick: callback,
      tooltip: 'Save as Serverless Functions'
    });

    panel.toolbar.addItem('severless-add', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}

/**
 * Manager Serverless Function
 */
export
class ButtonExtensionManager implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    let callback = () => {
      // NotebookActions.runAll(panel.content, context.session);
      const serverSettings = ServerConnection.makeSettings();
      FunctionRequest(null, serverSettings).then((data: any)=>{
            console.log(data)
            showDialog(new FunctionDialog(data.data))
          }
      )
    };
    let button = new ToolbarButton({
      className: 'serverless-manager',
      iconClassName: 'fa fa-tasks',
      onClick: callback,
      tooltip: 'Show Serverless Functions'
    });

    panel.toolbar.addItem('severless-manager', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}



function activate(app: JupyterFrontEnd) {
  // 注意 widgetName 为 Notebook
  app.serviceManager.nbconvert.getExportFormats()
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtensionAdd());
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtensionManager());
};

export default extension;
