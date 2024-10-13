public class Division extends Calculator{
    @Override
    Double compute(Double A, Double B) {
        if (B == 0) {
            System.out.println("Error, No division by zero");
            return 0.0;
        }
        try{
            Double result = A / B;
            return result;
        }catch(Exception e){
            System.out.println("Error,No division by zero");
            return 0.0;
        }
    }
}