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
import { useHistory, useParams } from "react-router-dom";
import { apiPrints, apiUnits, TGrade, TPrintDetail, TUnit } from "api";
import { RouterButton, RouterLink } from "components";

interface IFormInput {
  title: string;
  details: string[];
  question_count: string;
  action: string;
}

const backUrl = `/prints`;

function PrintForm() {
  const history = useHistory();
  const { printId } = useParams<{ printId: string }>();
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(false);
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

  const onSubmit: SubmitHandler<IFormInput> = async (formData) => {
    const params = {
      title: formData.title,
      details: formData.details
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
      const data =
        printId === "add"
          ? await apiPrints.create(params)
          : await apiPrints.update(printId, params);
      console.log(data);
      history.push(backUrl);
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
    let unmounted = false;
    const f = async () => {
      let _error = false;
      let _unitList: TUnit[] = [];
      let _title = "";
      let _details = [];
      try {
        _unitList = await apiUnits.list();
        if (printId !== "add") {
          const data = await apiPrints.get(printId);
          console.log(data);
          _title = data.title;
          _details = data.details;
        }
      } catch (error) {
        _error = true;
      }

      if (!unmounted) {
        setUnitList(_unitList);
        setValue("title", _title);
        let question_count = 0;
        _details.map((detail: TPrintDetail) => {
          _unitList.map((unit: TUnit, i: number) => {
            if (detail.unit === unit.id) {
              setValue(
                `details.${i}` as keyof IFormInput,
                `${detail.quantity}`
              );
              question_count += detail.quantity;
            }
            return false;
          });
          return false;
        });
        setValue("question_count", `${question_count}`);
        setFetchError(_error);
        setLoading(false);
      }
    };
    f();

    const cleanup = () => {
      unmounted = true;
    };
    return cleanup;
  }, [setValue, printId]);

  return (
    <form noValidate onSubmit={handleSubmit(onSubmit)}>
      <input
        style={{ display: "none" }}
        {...register("question_count", { required: true, min: 1 })}
        type="number"
      />
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12}>
          <Typography component="h2" variant="h6">
            プリントセットの{printId === "add" ? "追加" : "編集"}
          </Typography>
        </Grid>
        {!loading &&
          (fetchError ? (
            <Grid item xs={12}>
              <div>対象データの取得に失敗しました。</div>
              <div>
                <RouterLink to={backUrl}>戻る</RouterLink>
              </div>
            </Grid>
          ) : (
            <>
              <Grid item xs={12}>
                <TextField
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
              <Grid item xs={12} sm={4}>
                <Box textAlign="center">全 {questionCount} 問</Box>
              </Grid>
              <Grid item xs={6} sm={4}>
                <RouterButton
                  fullWidth
                  variant="contained"
                  color="primary"
                  to={backUrl}
                >
                  キャンセル
                </RouterButton>
              </Grid>
              <Grid item xs={6} sm={4}>
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
            </>
          ))}
      </Grid>
    </form>
  );
}

export default PrintForm;
