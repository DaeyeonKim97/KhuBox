import React from 'react';
import { Switch, Redirect } from 'react-router-dom';

import { RouteWithLayout } from './components';
import { Main as MainLayout, Minimal as MinimalLayout } from './layouts';

import {
  Dashboard as DashboardView,
  RecentFileList as RecentFileListView,
  MyDrive as MyDriveView,
  SharedFileList as SharedFileView,
  Trash as TrashView,
  Icons as IconsView,
  Account as AccountView,
  Settings as SettingsView,
  SignUp as SignUpView,
  SignIn as SignInView,
  NotFound as NotFoundView
} from './views';

const Routes = () => {
  return (
    <Switch>
      <Redirect
        exact
        from="/"
        to="/my-drive"
      />
      <RouteWithLayout
        component={MyDriveView}
        exact
        layout={MainLayout}
        path="/my-drive"
      />
      <RouteWithLayout
        component={SharedFileView}
        exact
        layout={MainLayout}
        path="/share"
      />
      <RouteWithLayout
        component={RecentFileListView}
        exact
        layout={MainLayout}
        path="/recent"
      />
      <RouteWithLayout
        component={TrashView}
        exact
        layout={MainLayout}
        path="/trash"
      />
      <RouteWithLayout
        component={AccountView}
        exact
        layout={MainLayout}
        path="/account"
      />
      <RouteWithLayout
        component={SettingsView}
        exact
        layout={MainLayout}
        path="/settings"
      />
      <RouteWithLayout
        component={SignUpView}
        exact
        layout={MinimalLayout}
        path="/sign-up"
      />
      <RouteWithLayout
        component={SignInView}
        exact
        layout={MinimalLayout}
        path="/sign-in"
      />
      <RouteWithLayout
        component={NotFoundView}
        exact
        layout={MinimalLayout}
        path="/not-found"
      />
      <Redirect to="/not-found" />
    </Switch>
  );
};

export default Routes;