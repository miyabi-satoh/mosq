import {
  Grid,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
} from "@material-ui/core";
import { TArchive } from "api";
import { apiArchives } from "api/archives";
import { Spacer } from "components";
import { formatDistance } from "date-fns";
import { ja } from "date-fns/locale";
import { useState, useEffect } from "react";
import { Switch, Route } from "react-router-dom";

function Index() {
  const [archiveList, setArchiveList] =
    useState<TArchive[] | undefined>(undefined);

  const handleRemove = async (id: string) => {
    try {
      await apiArchives.delete(id);

      const data = await apiArchives.list();
      console.log(data);
      setArchiveList(data.results);
    } catch (error) {}
  };

  useEffect(() => {
    let unmounted = false;
    const f = async () => {
      try {
        const data = await apiArchives.list();
        console.log(data);

        if (!unmounted) {
          setArchiveList(data.results);
        }
      } catch (error) {}
    };
    f();

    const cleanup = () => {
      unmounted = true;
    };
    return cleanup;
  }, []);

  return (
    <Grid container spacing={2} alignItems="center">
      <Grid item xs={12} sm>
        <Typography component="h2" variant="h6">
          アーカイブ一覧
        </Typography>
      </Grid>
      <Grid item container>
        {archiveList?.length ? (
          archiveList.map((archive) => {
            return (
              <Grid item xs={12} sm={6} key={`archive-${archive.id}`}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography component="h3" variant="h5">
                      {archive.title}
                    </Typography>
                    <Typography color="textSecondary">
                      作成日：
                      {formatDistance(
                        new Date(archive.created_at),
                        new Date(),
                        {
                          locale: ja,
                          addSuffix: true,
                        }
                      )}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button
                      color="primary"
                      variant="outlined"
                      onClick={() => window.open(archive.file)}
                    >
                      印刷
                    </Button>
                    <Spacer />
                    <Button
                      color="secondary"
                      variant="outlined"
                      onClick={() => handleRemove(`${archive.id}`)}
                    >
                      削除
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            );
          })
        ) : (
          <Grid item xs={12}>
            <Box textAlign="center" py={4}>
              アーカイブはありません。
            </Box>
          </Grid>
        )}
      </Grid>
    </Grid>
  );
}

function Archives() {
  return (
    <Box mx={2}>
      <Switch>
        <Route component={Index} />
      </Switch>
    </Box>
  );
}

export default Archives;
