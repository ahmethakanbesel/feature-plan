import React, {useState, useEffect} from 'react'
import {useDispatch, useSelector} from 'react-redux'
import {Link} from 'react-router-dom'
import {Row, Col, Image, ListGroup, Button, Card, Form, InputGroup, FormControl} from 'react-bootstrap'
import Rating from '../components/Rating'
import Loader from '../components/Loader'
import Message from '../components/Message'
import Feature from '../components/Feature'
import {listProductDetails, createProductReview} from '../actions/productActions'
import {PRODUCT_CREATE_REVIEW_RESET} from '../constants/productConstants'

function ProductScreen({match, history}) {
    const [qty, setQty] = useState(1)
    const [rating, setRating] = useState(0)
    const [comment, setComment] = useState('')

    const dispatch = useDispatch()

    const productDetails = useSelector(state => state.productDetails)
    const {loading, error, product} = productDetails

    const userLogin = useSelector(state => state.userLogin)
    const {userInfo} = userLogin

    const productReviewCreate = useSelector(state => state.productReviewCreate)
    const {
        loading: loadingProductReview,
        error: errorProductReview,
        success: successProductReview,
    } = productReviewCreate

    useEffect(() => {
        if (successProductReview) {
            setRating(0)
            setComment('')
            dispatch({type: PRODUCT_CREATE_REVIEW_RESET})
        }

        dispatch(listProductDetails(match.params.id))

    }, [dispatch, match, successProductReview])

    const addToCartHandler = () => {
        history.push(`/cart/${match.params.id}?qty=${qty}`)
    }

    const submitHandler = (e) => {
        e.preventDefault()
        dispatch(createProductReview(
            match.params.id, {
                rating,
                comment
            }
        ))
    }
    // <span className="border border-dark rounded-circle h-100" style={{background:product.primaryColor}}/>
    const featureTypes = [];
    const featureStatuses = [];
    if (!loading && !error && product.features.length > 0) {
        product.featureTypes.forEach(async function (featureType) {
            featureTypes[featureType.id] = featureType
        })
        product.featureStatuses.forEach(async function (featureStatus) {
            featureStatuses[featureStatus.id] = featureStatus
        })
    }
    return (
        <div>
            <Link to='/' className='btn btn-light my-3'>Go Back</Link>
            {loading ?
                <Loader/>
                : error
                    ? <Message variant='danger'>{error}</Message>
                    : (
                        <div>
                            <Row style={{background: product.secondaryColor}} className='py-5'>
                                <Col sm={12} md={2} lg={2} className='mt-4'>
                                    {product.logo ? (<Image src={product.logo} className="rounded-circle h-50"
                                                            alt={product.name}/>) :
                                        <span style={{background: product.primaryColor}} className="product-circle"/>}

                                </Col>
                                <Col sm={12} md={8} lg={8} className='text-left'>
                                    <h1 className='text-capitalize'>{product.name}</h1>
                                    <p className='lead'>{product.description}</p>
                                </Col>
                                <Col sm={12} md={2} lg={2} className='float-right mt-4'>
                                    <a className='text-dark text-decoration-none' href={product.websiteUrl}><i className="fas fa-external-link-alt"/> Website</a>
                                </Col>
                            </Row>
                            <Row className='px-5 mt-4'>
                                <Col className='w-50'>
                                    <InputGroup className="mb-3">
                                        <FormControl
                                            placeholder="Search"
                                            aria-label="Search"
                                        />
                                        <Button variant="outline-secondary" id="button-addon2">
                                            <i className="fas fa-search"/>
                                        </Button>
                                    </InputGroup>
                                </Col>
                                <Col>
                                    <Form.Control as="select">
                                        <option value="deneme">Deneme</option>
                                    </Form.Control>
                                </Col>
                            </Row>

                            <div className='d-flex justify-content-center'>
                                <Row className='w-100 px-5 py-5'>
                                    <Col className='px-5'>
                                        {product.features.length === 0 && <Message variant='info'>No Reviews</Message>}
                                        <ListGroup variant='flush'>
                                            {product.features.map((feature) => (
                                                <ListGroup.Item key={feature.id}>
                                                    <Row className='border border-dark rounded py-5'>
                                                        <Col sm={6} md={10} lg={10}>
                                                            <strong className='font-weight-bold'>{feature.name}</strong>
                                                            <hr/>
                                                            <p>
                                                                <span className='badge p-2 rounded-pill text-white'
                                                                     style={{background: featureTypes[feature.type].color}}>{featureTypes[feature.type].name}</span> · <span
                                                                className='badge p-2 rounded-pill text-white'
                                                                style={{background: featureStatuses[feature.status].color}}>{featureStatuses[feature.status].name}</span>
                                                            </p>
                                                        </Col>
                                                        <Col className='text-center'>
                                                            <span className='text-center border border-dark border-1 rounded p-3 w-100'>{feature.votes}</span><br/>
                                                            <button className='btn btn-primary position-relative mt-3'>Vote</button>
                                                        </Col>
                                                    </Row>
                                                </ListGroup.Item>
                                            ))}
                                        </ListGroup>
                                    </Col>
                                </Row>
                            </div>
                            <Row>
                                <Col md={6}>
                                    <h4>Reviews</h4>
                                    {product.reviews.length === 0 && <Message variant='info'>No Reviews</Message>}

                                    <ListGroup variant='flush'>
                                        {product.reviews.map((review) => (
                                            <ListGroup.Item key={review._id}>
                                                <strong>{review.name}</strong>
                                                <Rating value={review.rating} color='#f8e825' />
                                                <p>{review.createdAt.substring(0, 10)}</p>
                                                <p>{review.comment}</p>
                                            </ListGroup.Item>
                                        ))}

                                        <ListGroup.Item>
                                            <h4>Write a review</h4>

                                            {loadingProductReview && <Loader />}
                                            {successProductReview && <Message variant='success'>Review Submitted</Message>}
                                            {errorProductReview && <Message variant='danger'>{errorProductReview}</Message>}

                                            {userInfo ? (
                                                <Form onSubmit={submitHandler}>
                                                    <Form.Group controlId='rating'>
                                                        <Form.Label>Rating</Form.Label>
                                                        <Form.Control
                                                            as='select'
                                                            value={rating}
                                                            onChange={(e) => setRating(e.target.value)}
                                                        >
                                                            <option value=''>Select...</option>
                                                            <option value='1'>1 - Poor</option>
                                                            <option value='2'>2 - Fair</option>
                                                            <option value='3'>3 - Good</option>
                                                            <option value='4'>4 - Very Good</option>
                                                            <option value='5'>5 - Excellent</option>
                                                        </Form.Control>
                                                    </Form.Group>

                                                    <Form.Group controlId='comment'>
                                                        <Form.Label>Review</Form.Label>
                                                        <Form.Control
                                                            as='textarea'
                                                            row='5'
                                                            value={comment}
                                                            onChange={(e) => setComment(e.target.value)}
                                                        ></Form.Control>
                                                    </Form.Group>

                                                    <Button
                                                        disabled={loadingProductReview}
                                                        type='submit'
                                                        variant='primary'
                                                    >
                                                        Submit
                                                    </Button>

                                                </Form>
                                            ) : (
                                                    <Message variant='info'>Please <Link to='/login'>login</Link> to write a review</Message>
                                                )}
                                        </ListGroup.Item>
                                    </ListGroup>
                                </Col>
                            </Row>
                        </div>
                    )
            }
        </div>
    )
}

export default ProductScreen
