import React, { useState } from 'react';
import { makeStyles } from '@material-ui/styles';

import { TrashToolbar, RemovedFileTable } from './components';
import mockData from './data';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  content: {
    marginTop: theme.spacing(2)
  }
}));

const Trash = () => {
  const classes = useStyles();

  const [files] = useState(mockData);

  return (
    <div className={classes.root}>
      <TrashToolbar />
      <div className={classes.content}>
        <RemovedFileTable files={files} />
      </div>
    </div>
  );
};

export default Trash;
