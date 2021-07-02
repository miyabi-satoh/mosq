import {
  Box,
  Button,
  Checkbox,
  createStyles,
  Divider,
  FormControlLabel,
  Grid,
  makeStyles,
  TextField,
  Theme,
  Typography,
} from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { apiPrints, TPrintHead } from "api";
import { Indicator, RouterLink } from "components";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    listUnits: {
      paddingLeft: theme.spacing(4),
    },
  })
);

const Cookies = () => {
  const { cookie } = document;
  const cookieMap = new Map();
  if (!cookie) return cookieMap;
  const cookies = cookie.split("; ");
  cookies.forEach((c) => {
    const item = c.split("=");
    cookieMap.set(item[0], decodeURIComponent(item[1]));
  });
  return cookieMap;
};

export default function PrintOut() {
  const classes = useStyles();
  const { printId } = useParams<{ printId: string }>();
  const [data, setData] = useState<TPrintHead | undefined | null>(undefined);

  useEffect(() => {
    let unmounted = false;
    const f = async () => {
      let _data: TPrintHead | null = null;
      try {
        _data = await apiPrints.get(printId);
        console.log(_data);
      } catch (error) {
      } finally {
        if (!unmounted) {
          setData(_data);
        }
      }
    };
    f();

    return () => {
      unmounted = true;
    };
  }, [printId]);

  if (data === undefined) {
    return <Indicator />;
  }

  if (data === null) {
    return <Alert severity="error">プリントデータが存在しません。</Alert>;
  }

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <RouterLink to="/prints">戻る</RouterLink>
      </Grid>
      <Grid item xs={12} sm={6}>
        <form action="/printout/" method="post" target="_blank">
          <input type="hidden" name="printhead" value={data.id} />
          <input
            type="hidden"
            name="csrfmiddlewaretoken"
            value={Cookies().get("csrftoken")}
          />
          <Box my={2}>
            <TextField
              id="title"
              name="title"
              label="タイトル"
              variant="outlined"
              size="small"
              defaultValue={data.title}
              fullWidth
            />
          </Box>
          <Box my={2}>
            <FormControlLabel
              control={<Checkbox name="archive" value={true} />}
              label="アーカイブに登録する"
            />
          </Box>
          <Box my={2}>
            <Button type="submit" color="primary" variant="contained">
              印刷
            </Button>
          </Box>
        </form>
      </Grid>
      <Grid item xs={12} sm={6}>
        <Box mb={2}>
          <Typography variant="subtitle1" component="h2">
            タイトル
          </Typography>
          <Divider />
          <Box m={2} my={1}>
            {data.title}
          </Box>
        </Box>
        <Box my={2}>
          <Typography variant="subtitle1" component="h3">
            説明
          </Typography>
          <Divider />
          <Box m={2} my={1}>
            {data.description}
          </Box>
        </Box>
        <Box my={2}>
          <Typography variant="subtitle1" component="h3">
            プリント形式
          </Typography>
          <Divider />
          <Box m={2} my={1}>
            {data.printtype.type_text}
          </Box>
        </Box>
        <Box my={2}>
          <Typography variant="subtitle1" component="h4">
            単元と問題数
          </Typography>
          <Divider />
          <Box my={1}>
            <ul className={classes.listUnits}>
              {data.details.map((detail, i) => {
                return (
                  <li key={i}>
                    {detail.units
                      .map((u) => {
                        return `${u.unit_text}(${u.grade.grade_text})`;
                      })
                      .join(", ")}
                    から {detail.quantity}問
                  </li>
                );
              })}
            </ul>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
