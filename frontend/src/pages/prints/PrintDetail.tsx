import { Box, Divider, Typography } from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { apiPrints, TPrintHead } from "api";
import { Indicator, RouterLink } from "components";
import { logger } from "helper";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function PrintDetail() {
  const { printId } = useParams<{ printId: string }>();
  const [data, setData] = useState<TPrintHead | undefined | null>(undefined);

  useEffect(() => {
    let unmounted = false;
    const f = async () => {
      let _data: TPrintHead | null = null;
      try {
        _data = await apiPrints.get(printId);
        logger(_data);
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
    <>
      <Box mb={2}>
        <RouterLink to="/prints">戻る</RouterLink>
      </Box>
      <Typography variant="subtitle1" component="h2">
        タイトル
      </Typography>
      <Divider />
      <Box m={2} mt={1} mb={4}>
        {data.title}
      </Box>
      <Typography variant="subtitle1" component="h3">
        説明
      </Typography>
      <Divider />
      <Box m={2} mt={1} mb={4}>
        {data.description}
      </Box>
      <Typography variant="subtitle1" component="h3">
        プリント形式
      </Typography>
      <Divider />
      <Box m={2} mt={1} mb={4}>
        {data.printtype.type_text}
      </Box>
      <Typography variant="subtitle1" component="h4">
        単元と問題数
      </Typography>
      <Divider />
      <Box m={2} mt={1} mb={4}>
        {data.details.map((detail, i) => {
          return (
            <div key={i}>
              {detail.units
                .map((u) => {
                  return `${u.unit_text}(${u.grade.grade_text})`;
                })
                .join(", ")}
              から {detail.quantity}問
            </div>
          );
        })}
      </Box>
    </>
  );
}
