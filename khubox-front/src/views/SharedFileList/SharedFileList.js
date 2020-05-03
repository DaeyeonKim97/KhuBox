import React, { useState } from 'react';
import { makeStyles } from '@material-ui/styles';

import { SharedFileToolbar, SharedFileTable } from './components';
import mockData from './data';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  content: {
    marginTop: theme.spacing(2)
  }
}));

const SharedFileList = () => {
  const classes = useStyles();

  const [files] = useState(mockData);

  return (
    <div className={classes.root}>
      <SharedFileToolbar />
      <div className={classes.content}>
        <SharedFileTable files={files} />
      </div>
    </div>
  );
};

export default SharedFileList;
