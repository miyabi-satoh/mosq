import {
  Box,
  Button,
  Grid,
  InputAdornment,
  TextField,
  Typography,
} from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import { useEffect, useState } from "react";
import { SubmitHandler, useForm, useWatch } from "react-hook-form";
import { Link, useParams } from "react-router-dom";
import { MainLayout } from "layouts/MainLayout";
import { apiPrints, apiUnits, TGrade, TUnit } from "api";

interface IFormInput {
  title: string;
  details: string[];
  question_count: string;
  action: string;
}

function PrintForm() {
  const { printId } = useParams<{ printId: string }>();
  const [error, setError] = useState(false);
  const [unitList, setUnitList] = useState<TUnit[]>([]);
  const {
    register,
    control,
    handleSubmit,
    getValues,
    setValue,
    formState: { errors },
  } = useForm<IFormInput>();
  const questionCount = useWatch({
    control,
    name: "question_count",
    defaultValue: "0",
  });

  const onSubmit: SubmitHandler<IFormInput> = async (data) => {
    const params = {
      title: data.title,
      details: data.details
        .filter((strValue) => strValue)
        .map((strValue, i) => {
          return {
            unit: unitList[i].id,
            quantity: strValue,
          };
        }),
    };
    console.log(params);
    try {
      const resp = await apiPrints.create(params);
      console.log(resp.data);
      if (data.action === "print") {
        // window.open("http://localhost:8000/", "_blank");
      }
    } catch (error) {}
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const details = getValues("details");
    const question_count = details.reduce((prev, current) => {
      const value = Number(current);
      return isNaN(value) ? prev : prev + value;
    }, 0);
    setValue("question_count", `${question_count}`);
  };

  useEffect(() => {
    async function fetchUnits() {
      try {
        setUnitList(await apiUnits.list());
        if (printId !== "add") {
          const data = await apiPrints.get(Number(printId));
          setValue("title", data.title);
        }
      } catch (error) {
        if (error?.response?.status === 404) {
          setError(true);
        }
      }
    }
    fetchUnits();
  }, [setValue, printId]);

  return (
    <MainLayout>
      <form noValidate onSubmit={handleSubmit(onSubmit)}>
        <input
          style={{ display: "none" }}
          {...register("question_count", { required: true, min: 1 })}
          type="number"
        />
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12}>
            <Typography component="h2" variant="h6">
              プリント{printId === "add" ? "追加" : "編集"}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              size="small"
              inputProps={{
                ...register("title", {
                  required: true,
                }),
              }}
              label="プリントのタイトル"
              error={!!errors.title}
              fullWidth
              autoFocus
              required
            />
          </Grid>
          {unitList.map((unit: TUnit, i: number) => {
            const grade = unit.grade as TGrade;
            return (
              <Grid item xs={12} sm={6} md={4} key={`unit-${i}`}>
                <Box display="flex" alignItems="center">
                  <TextField
                    variant="outlined"
                    size="small"
                    type="number"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          {`${grade.grade_text}:${unit.unit_text}(${unit.question_count})`}
                        </InputAdornment>
                      ),
                    }}
                    inputProps={{
                      ...register(`details.${i}` as keyof IFormInput, {
                        min: 0,
                        max: unit.question_count,
                      }),
                      min: 0,
                      max: unit.question_count,
                      style: { textAlign: "right" },
                    }}
                    onChange={handleChange}
                    disabled={unit.question_count === 0}
                    fullWidth
                  />
                </Box>
              </Grid>
            );
          })}
          {errors.question_count && (
            <Grid item xs={12}>
              <Alert severity="error">問題数を設定してください。</Alert>
            </Grid>
          )}
          {errors.title && (
            <Grid item xs={12}>
              <Alert severity="error">
                プリントのタイトルを入力してください。
              </Alert>
            </Grid>
          )}
          <Grid item container spacing={2} alignItems="center">
            <Grid item xs={12} sm>
              <Box textAlign="center">全 {questionCount} 問</Box>
            </Grid>
            <Grid item xs>
              <Button
                fullWidth
                variant="contained"
                color="primary"
                component={Link}
                to="/prints"
              >
                戻る
              </Button>
            </Grid>
            <Grid item sm>
              <Button
                fullWidth
                variant="contained"
                color="secondary"
                type="submit"
                onClick={() => setValue("action", "print")}
              >
                保存して印刷
              </Button>
            </Grid>
            <Grid item xs>
              <Button
                fullWidth
                variant="contained"
                color="secondary"
                type="submit"
                onClick={() => setValue("action", "save")}
              >
                保存
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </form>
    </MainLayout>
  );
}

export default PrintForm;
