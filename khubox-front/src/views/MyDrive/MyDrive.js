import React, { useState } from 'react';
import { makeStyles } from '@material-ui/styles';

import { DriveToolbar, FileTable } from './components';
import mockData from './data';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  content: {
    marginTop: theme.spacing(2)
  }
}));

const MyDrive = () => {
  const classes = useStyles();

  const [files] = useState(mockData);

  return (
    <div className={classes.root}>
      <DriveToolbar />
      <div className={classes.content}>
        <FileTable files={files} />
      </div>
    </div>
  );
};

export default MyDrive;
